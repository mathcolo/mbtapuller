from geopy.distance import vincenty as dist
from Classes import Station, Trip, TripRecord
from sqlalchemy.sql.expression import func

def is_red_braintree(origin, destination):
    return origin.name_human_readable == 'Braintree' or destination.name_human_readable == 'Braintree'

def is_red_ashmont(origin, destination):
    return origin.name_human_readable == 'Ashmont' or destination.name_human_readable == 'Ashmont'

def braintree_only_stations():
    return ['North Quincy', 'Wollaston', 'Quincy Center', 'Quincy Adams', 'Braintree']

def ashmont_only_stations():
    return ['Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont']

def surrounding_station(session, station):
    '''

    :param session: The database session to operate with
    :param station: The station in question
    :return: A 2-element tuple containing the forward and backward station
    '''

    max = session.query(func.max(Station.id)).filter_by(Station.route == station.route)
    min = session.query(func.min(Station.id)).filter_by(Station.route == station.route)
    if station.route != 'Red':
        plus_id = station.id + 1
        if plus_id > max:
            plus_id = max

        minus_id = station.id - 1
        if minus_id < min:
            minus_id = min
    else:
        # Red Line

        pass

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

        # Red Line override
        if is_red_braintree(origin_station, destination_station):
            if station.name_human_readable in ashmont_only_stations():
                continue

        if is_red_ashmont(origin_station, destination_station):
            if station.name_human_readable in braintree_only_stations():
                continue

        station_loc = (station.location_lat, station.location_lng)
        miles = dist(me_loc, station_loc).miles
        if miles < closest_distance_so_far:
            closest_station = station
            closest_distance_so_far = miles

    #print "closest_station: %s" % closest_station
    surround_station_1 = session.query(Station).filter(Station.id == closest_station.id+1).first()

    if closest_station.id == 1:
        surround_station_2 = closest_station
    else:
        surround_station_2 = session.query(Station).filter(Station.id == closest_station.id-1).first()

    #print "surround_station_1: %s" % surround_station_1
    #print "surround_station_2: %s" % surround_station_2

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