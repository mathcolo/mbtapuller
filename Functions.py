from geopy.distance import vincenty as dist
from Classes import Station, Trip, TripRecord, Route
from sqlalchemy import desc, asc, or_
import constants

def surrounding_station(session, station):
    '''
    Return surrounding stations for this station

    :param session: The database session to operate with
    :param station: The station in question
    :return: A 2-element tuple containing the forward and backward station
    '''

    max = session.query(Station).filter(Station.route == station.route).order_by(desc(Station.id)).first().id
    min = session.query(Station).filter(Station.route == station.route).order_by(asc(Station.id)).first().id

    plus_id = station.id + 1
    if plus_id > max:
        plus_id = max

    minus_id = station.id - 1
    if minus_id < min:
        minus_id = min

    return (session.query(Station).filter(Station.id == plus_id).first(),
           session.query(Station).filter(Station.id == minus_id).first())


def find_segment(trip_record, session, test_pair=None):

    if test_pair:
        me_loc = test_pair
    else:
        me_loc = (trip_record.location_lat, trip_record.location_lng)

    trip = session.query(TripRecord, Trip).join(Trip).filter(Trip.id == trip_record.trip_id).first()[1]

    origin_station = session.query(Station).filter(Station.id == trip.origin_station_id).first()
    destination_station = session.query(Station).filter(Station.id == trip.destination_station_id).first()

    print "origin_station: %s" % origin_station
    print "destination_station: %s" % destination_station

    all_stations = session.query(Station).filter(Station.route == origin_station.route).all()
    closest_station = None
    closest_distance_so_far = 100
    for station in all_stations:

        station_loc = (station.location_lat, station.location_lng)
        miles = dist(me_loc, station_loc).miles
        if miles < closest_distance_so_far:
            closest_station = station
            closest_distance_so_far = miles

    surrounding_stations = surrounding_station(session, closest_station)
    surround_station_1 = surrounding_stations[1]
    surround_station_2 = surrounding_stations[0]

    if dist(surround_station_1.loc(), destination_station.loc()) < dist(surround_station_2.loc(), destination_station.loc()):
        surround_station_ahead = surround_station_1
        surround_station_behind = surround_station_2
    else:
        surround_station_ahead = surround_station_2
        surround_station_behind = surround_station_1

    if dist(me_loc, destination_station.loc()) < dist(closest_station.loc(), destination_station.loc()):
        return closest_station.name_human_readable, surround_station_ahead.name_human_readable
    else:
        return surround_station_behind.name_human_readable, closest_station.name_human_readable

def all_routes(session):
    routes = session.query(Route).all()
    routes_output = []
    for route in routes:
        routes_output.append({'id': route.id, 'name': route.name})

    return routes_output


def get_stations(route, session):
    if route.lower() == constants.RED_LINE.lower():

        start_id = session.query(Station).filter(Station.name_api == 'place-alfcl').one().id

        braintree = session.query(Station).filter(Station.route == route.title()).filter(or_(Station.id > start_id + 16, Station.id < start_id + 13)).order_by(Station.id).all()
        ashmont = session.query(Station).filter(Station.route == route.title()).filter(Station.id < start_id + 17).all()

        braintree_names = [b.name_human_readable for b in braintree]
        ashmont_names = [a.name_human_readable for a in ashmont]

        return {'line': constants.RED_LINE, 'branches': [{'name': 'Ashmont', 'stations': ashmont_names},
                                                        {'name': 'Braintree', 'stations': braintree_names}]}

    elif route.lower() == constants.GREEN_LINE.lower():

        b_line = session.query(Station).filter(Station.route == constants.GREEN_LINE_B).all()
        c_line = session.query(Station).filter(Station.route == constants.GREEN_LINE_C).all()
        d_line = session.query(Station).filter(Station.route == constants.GREEN_LINE_D).all()
        e_line = session.query(Station).filter(Station.route == constants.GREEN_LINE_E).all()

        b_names = [b.name_human_readable for b in b_line]
        c_names = [c.name_human_readable for c in c_line]
        d_names = [d.name_human_readable for d in d_line]
        e_names = [e.name_human_readable for e in e_line]

        stations = {'line': constants.GREEN_LINE,  'branches': [{'name': constants.GREEN_LINE_B, 'stations': b_names},
                                                                {'name': constants.GREEN_LINE_C, 'stations': c_names},
                                                                {'name': constants.GREEN_LINE_D, 'stations': d_names},
                                                                {'name': constants.GREEN_LINE_E, 'stations': e_names}]}

        return stations

    elif route.lower() in [constants.ORANGE_LINE.lower(), constants.BLUE_LINE.lower()]:
        stations = session.query(Station).filter(Station.route == route.title()).all()

        return {'line': route.title(), 'branches': [{'name': '', 'stations': [s.name_human_readable for s in stations]}]}

    return None