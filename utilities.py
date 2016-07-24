import constants
import db_objects as db

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

def origin_and_destination_stations(session, api_trip, route_name):

    if route_name == 'Red':
        if string_contains_ashmont_anything(api_trip['trip_name']):
            route_name = constants.RED_LINE_ASHMONT
        elif string_contains_braintree_anything(api_trip['trip_name']):
            route_name = constants.RED_LINE_BRAINTREE
        else:
            route_name = constants.RED_LINE_ASHMONT

    route_id = session.query(db.Route).filter(db.Route.name == route_name).first().id

    origin_station_id = session.query(db.Station).filter(db.Station.route_id == route_id).filter(
        db.Station.name_human_readable == isolate_origin_from_trip_name(api_trip['trip_name'])).first().id
    destination_station_id = session.query(db.Station).filter(db.Station.route_id == route_id).filter(
        db.Station.name_human_readable == api_trip['trip_headsign']).first().id

    return origin_station_id, destination_station_id