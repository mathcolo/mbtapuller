import datetime
import API
from Classes import Station, Trip, TripRecord, Route
from Miscellaneous import isolate_origin_from_trip_name
from constants import *

def get_routes():
    routes = [
        Route(name=RED_LINE_ASHMONT),
        Route(name=RED_LINE_BRAINTREE),
        Route(name=GREEN_LINE_B),
        Route(name=GREEN_LINE_C),
        Route(name=GREEN_LINE_D),
        Route(name=GREEN_LINE_E),
        Route(name=BLUE_LINE),
        Route(name=ORANGE_LINE),
    ]

    return routes

def get_stations(session):
    stations = []
    routes = session.query(Route).all()

    populate_red = False

    for route in routes:
        if route.name == RED_LINE_ASHMONT or route.name == RED_LINE_BRAINTREE:
            populate_red = True
            continue

        api_result = API.get("stopsbyroute", {'route': route.name})['direction'][0]['stop']
        for item in api_result:
            new_station = Station(route_id=route.id, name_human_readable=item['parent_station_name'], name_api=item['parent_station'], location_lat=item['stop_lat'], location_lng=item['stop_lon'])
            stations.append(new_station)

    if populate_red:
        ashmont = []
        ashmont_added_jfk = False
        braintree = []
        braintree_added_jfk = False

        route_id_ashmont = session.query(Route).filter(Route.name == RED_LINE_ASHMONT).first().id
        route_id_braintree = session.query(Route).filter(Route.name == RED_LINE_BRAINTREE).first().id

        api_result = API.get("stopsbyroute", {'route': 'Red'})['direction'][0]['stop']
        for item in api_result:

            if item['parent_station_name'] in ['North Quincy', 'Wollaston', 'Quincy Center', 'Quincy Adams', 'Braintree']:
                new_station = Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                braintree.append(new_station)
            elif item['parent_station_name'] in ['Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont']:
                new_station = Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                ashmont.append(new_station)
            else:
                new_station_ashmont = Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                new_station_braintree = Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])

                if new_station_ashmont.name_api == 'place-jfk':
                    if not ashmont_added_jfk:
                        ashmont_added_jfk = True
                        ashmont.append(new_station_ashmont)
                else:
                    ashmont.append(new_station_ashmont)

                if new_station_braintree.name_api == 'place-jfk':
                    if not braintree_added_jfk:
                        braintree_added_jfk = True
                        braintree.append(new_station_braintree)
                else:
                    braintree.append(new_station_braintree)

        stations.extend(ashmont)
        stations.extend(braintree)

    return stations


def sync_trips_and_records(routes, session):

    print "Syncing trips..."

    to_save = []

    route_string = ",".join(routes)
    data = API.get("vehiclesbyroutes", {'routes': route_string})
    mode = data['mode']
    for route in mode:
        route_sub = route['route']
        for direction in route_sub[0]['direction']:
            for trip in direction['trip']:
                # Now we have a trip
                print "Processing trip_id %s" % trip['trip_id']

                trips_with_same_id = session.query(Trip).filter(Trip.id.is_(trip['trip_id'])).filter(
                    Trip.date.is_(datetime.date.today())).count()
                if trips_with_same_id == 1:
                    # Create a trip record since it exists already

                    new_trip_record = TripRecord(trip_id=trip['trip_id'], location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                    to_save.append(new_trip_record)
                elif trips_with_same_id == 0:

                    origin_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(isolate_origin_from_trip_name(trip['trip_name']))).first().id
                    destination_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(trip['trip_headsign'])).first().id

                    new_trip = Trip(id=trip['trip_id'], origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                                    date=datetime.datetime.now())

                    new_trip_record = TripRecord(trip_id=trip['trip_id'], location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                    to_save.append(new_trip)
                    to_save.append(new_trip_record)

                else:
                    raise RuntimeError("There were multiple trip objects with the same id: %s" % trips_with_same_id)

    for object in to_save:
        session.merge(object)

    return to_save
