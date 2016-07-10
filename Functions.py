from geopy.distance import vincenty
from Classes import Station, Route
import constants
from sqlalchemy import or_

def current_station(trip_record, session):
    """
    Find the current station that a TripRecord is at.

    Example return: Harvard station object, Alewife station object
    Example if the train is not within 400 of a station: None

    :param trip_record: The TripRecord object to evaluate.
    :param session: The database session to use for data queries
    :return: A Station object
    """
    all_stations = session.query(Station).all()
    for station in all_stations:
        us = (trip_record.location_lat, trip_record.location_lng)
        it = (station.location_lat, station.location_lng)

        if vincenty(us, it).feet <= 400:
            return station

    return None


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