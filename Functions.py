from geopy.distance import vincenty
from geopy.distance import vincenty as dist
from sqlalchemy import desc, asc, or_
import Classes as c
import constants

def surrounding_station(session, station):
    '''
    Return surrounding stations for this station

    :param session: The database session to operate with
    :param station: The station in question
    :return: A 2-element tuple containing the forward and backward station
    '''

    max = session.query(c.Station).filter(c.Station.route_id == station.route_id).order_by(desc(c.Station.id)).first().id
    min = session.query(c.Station).filter(c.Station.route_id == station.route_id).order_by(asc(c.Station.id)).first().id

    plus_id = station.id + 1
    if plus_id > max:
        plus_id = max

    minus_id = station.id - 1
    if minus_id < min:
        minus_id = min

    return (session.query(c.Station).filter(c.Station.id == plus_id).first(),
           session.query(c.Station).filter(c.Station.id == minus_id).first())


def find_segment(trip_record, session, test_pair=None):

    if test_pair:
        me_loc = test_pair
    else:
        me_loc = (trip_record.location_lat, trip_record.location_lng)

    trip = session.query(c.TripRecord, c.Trip).join(c.Trip).filter(c.Trip.id == trip_record.trip_id).first()[1]

    origin_station = session.query(c.Station).filter(c.Station.id == trip.origin_station_id).first()
    destination_station = session.query(c.Station).filter(c.Station.id == trip.destination_station_id).first()

    # print "origin_station: %s" % origin_station
    # print "destination_station: %s" % destination_station

    all_stations = session.query(c.Station).filter(c.Station.route_id == origin_station.route_id).all()
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

    # print "surround_station_1: %s" % surround_station_1
    # print "surround_station_2: %s" % surround_station_2

    if dist(surround_station_1.loc(), destination_station.loc()) < dist(surround_station_2.loc(), destination_station.loc()):
        surround_station_ahead = surround_station_1
        surround_station_behind = surround_station_2
    else:
        surround_station_ahead = surround_station_2
        surround_station_behind = surround_station_1

    if dist(me_loc, destination_station.loc()) < dist(closest_station.loc(), destination_station.loc()):
        return closest_station, surround_station_ahead
    else:
        return surround_station_behind, closest_station

def all_routes(session):
    routes = session.query(c.Route).all()
    routes_output = []
    for route in routes:
        routes_output.append({'id': route.id, 'name': route.name})

    return routes_output
	
def get_stations(id, session):

	stations = session.query(c.Station, c.Route).join(c.Route).filter(c.Station.route_id == id).all()
	
	route_name = session.query(c.Route).filter(c.Route.id == id).one().name
	
	stations_output = []
	for station in stations:
		stations_output.append({'id': station[0].id, 'route_id': station[0].route_id, 'name': station[0].name_human_readable, 'route_name': route_name})
			
	return stations_output

	
def getIdForRoute(name, session):
	print name
	id = session.query(c.Route).filter(c.Route.name == name).one().id
		
	return id


