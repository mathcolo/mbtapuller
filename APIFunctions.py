import Logger
import datetime
import API
import Classes as c
from Miscellaneous import origin_and_destination_stations
from constants import *

def get_routes():
    routes = [
        c.Route(name=RED_LINE_ASHMONT),
        c.Route(name=RED_LINE_BRAINTREE),
        c.Route(name=GREEN_LINE_B),
        c.Route(name=GREEN_LINE_C),
        c.Route(name=GREEN_LINE_D),
        c.Route(name=GREEN_LINE_E),
        c.Route(name=BLUE_LINE),
        c.Route(name=ORANGE_LINE),
    ]

    return routes

def get_stations(session):
    stations = []
    routes = session.query(c.Route).all()

    populate_red = False

    for route in routes:
        if route.name == RED_LINE_ASHMONT or route.name == RED_LINE_BRAINTREE:
            populate_red = True
            continue

        api_result = API.get("stopsbyroute", {'route': route.name})['direction'][0]['stop']
        for item in api_result:
            new_station = c.Station(route_id=route.id, name_human_readable=item['parent_station_name'], name_api=item['parent_station'], location_lat=item['stop_lat'], location_lng=item['stop_lon'])
            stations.append(new_station)

    if populate_red:
        ashmont = []
        ashmont_added_jfk = False
        braintree = []
        braintree_added_jfk = False

        route_id_ashmont = session.query(c.Route).filter(c.Route.name == RED_LINE_ASHMONT).first().id
        route_id_braintree = session.query(c.Route).filter(c.Route.name == RED_LINE_BRAINTREE).first().id

        api_result = API.get("stopsbyroute", {'route': 'Red'})['direction'][0]['stop']
        for item in api_result:

            if item['parent_station_name'] in RED_LINE_BRAINTREE_STATIONS:
                new_station = c.Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                braintree.append(new_station)
            elif item['parent_station_name'] in RED_LINE_ASHMONT_STATIONS:
                new_station = c.Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                ashmont.append(new_station)
            else:
                new_station_ashmont = c.Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                new_station_braintree = c.Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
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

    Logger.log.info("Syncing trips...")
    Logger.log.info("Input routes: %s" % routes)

    if 'Red-Ashmont' in routes or 'Red-Braintree' in routes:
        routes.remove('Red-Ashmont')
        routes.remove('Red-Braintree')
        routes.append('Red')

    Logger.log.info("Using routes: %s" % routes)

    to_save = []

    route_string = ",".join(routes)
    data = API.get("vehiclesbyroutes", {'routes': route_string})
    mode = data['mode']
    for route in mode:
        route_sub = route['route']
        for route_sub_sub in route_sub:
            route_name = route_sub_sub['route_id']
            Logger.log.info("Processing route %s" % route_name)
            for direction in route_sub_sub['direction']:
                for trip in direction['trip']:

                    # The MBTA sometimes just throws us random bs
                    # Love you guys, but...really?
                    if trip['trip_name'] == u'':
                        continue

                    trip['trip_name'] = trip['trip_name'].replace('Forest Hills Orange Line', 'Forest Hills')

                    # Now we have a trip
                    #print "Processing trip_id %s" % trip['trip_id']

                    trips_with_same_id = session.query(c.Trip).filter(c.Trip.api_id == str(trip['trip_id'])).filter(
                        c.Trip.date == datetime.date.today())
                    #print "trips_with_same_id is %s" % trips_with_same_id.count()
                    if trips_with_same_id.count() == 1:
                        # Create a trip record since it exists already

                        new_trip_record = c.TripRecord(trip_id=trips_with_same_id.first().id, location_lat=trip['vehicle']['vehicle_lat'],
                                                     location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                        to_save.append(new_trip_record)
                    elif trips_with_same_id.count() == 0:

                        station_pair = origin_and_destination_stations(session, trip, route_name)

                        origin_station_id = station_pair[0]
                        destination_station_id = station_pair[1]

                        new_trip = c.Trip(api_id=trip['trip_id'], origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                                        date=datetime.datetime.now())

                        session.add(new_trip)
                        session.commit()

                        new_trip_record = c.TripRecord(trip_id=new_trip.id, location_lat=trip['vehicle']['vehicle_lat'],
                                                     location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                        to_save.append(new_trip_record)

                    else:
                        raise RuntimeError("There were multiple trip objects with the same id: %s" % trips_with_same_id)

    for object in to_save:
        session.merge(object)

    session.commit()

    return to_save
