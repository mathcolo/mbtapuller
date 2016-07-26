import constants
import db_objects as db
from difflib import SequenceMatcher

def string_contains_ashmont_anything(string):
    for station_str in constants.RED_LINE_ASHMONT_STATIONS:
        if station_str in string:
            return True
    return False

def string_contains_braintree_anything(string):
    for station_str in constants.RED_LINE_BRAINTREE_STATIONS:
        if station_str in string:
            return True
    return False

def isolate_origin_from_trip_name(name):
    """
    Isolates origin station name from trip name.

    Example:
    '8:10 pm from Ashmont - Inbound to Alewife' returns 'Ashmont'

    :param name: Trip name as a string
    :return: Origin station name
    """

    if 'from' in name:
        return name[name.index('from') + 4:name.index(' to')].strip().split('-')[0].strip()
    else:
        return name.split(' to ')[0]

def isolate_destination_from_trip_name(name):
    """
    Isolates destination station name from trip name.

    Example:
    '8:10 pm from Ashmont - Inbound to Alewife' returns 'Alewife'

    :param name: Trip name as a string
    :return: Destination station name
    """

    if 'from' in name:
        return name[name.index('to')+2:].strip().split('-')[0].strip()
    else:
        return name.split(' to ')[1]

def origin_and_destination_stations(session, api_trip, route_id):
    origin_station_id = session.query(db.Station).filter(db.Station.route_id == route_id).filter(
        db.Station.name_human_readable == isolate_origin_from_trip_name(api_trip['trip_name'])).first().id
    destination_station_id = session.query(db.Station).filter(db.Station.route_id == route_id).filter(
        db.Station.name_human_readable == api_trip['trip_headsign']).first().id

    return origin_station_id, destination_station_id

def station_with_most_similar_name(session, route_id, name):
    
    stations = session.query(db.Station).filter(db.Station.route_id == route_id).all()
    
    longest_len = 0
    longest_name = ""
    longest_id = -1
    for s in stations:
        sm = SequenceMatcher(None, s.name_human_readable, name)
        
        k = sm.ratio()*100; 
        if k > longest_len:
            longest_len = k
            longest_id = s.id
            longest_name = s.name_human_readable
            
    return longest_id