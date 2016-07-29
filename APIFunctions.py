import Logger
import datetime
import API
import db_objects as db
from utilities import *
from constants import *

def get_routes():
    routes = [
        db.Route(name=RED_LINE_ASHMONT),
        db.Route(name=RED_LINE_BRAINTREE),
        db.Route(name=GREEN_LINE_B),
        db.Route(name=GREEN_LINE_C),
        db.Route(name=GREEN_LINE_D),
        db.Route(name=GREEN_LINE_E),
        db.Route(name=BLUE_LINE),
        db.Route(name=ORANGE_LINE),
    ]

    return routes

def get_stations(session):
    stations = []
    routes = session.query(db.Route).all()

    populate_red = False

    for route in routes:
        if route.name == RED_LINE_ASHMONT or route.name == RED_LINE_BRAINTREE:
            populate_red = True
            continue

        api_result = API.get("stopsbyroute", {'route': route.name})['direction'][0]['stop']
        for item in api_result:
            new_station = db.Station(route_id=route.id, name_human_readable=item['parent_station_name'], name_api=item['parent_station'], location_lat=item['stop_lat'], location_lng=item['stop_lon'])
            stations.append(new_station)

    if populate_red:
        ashmont = []
        ashmont_added_jfk = False
        braintree = []
        braintree_added_jfk = False

        route_id_ashmont = session.query(db.Route).filter(db.Route.name == RED_LINE_ASHMONT).first().id
        route_id_braintree = session.query(db.Route).filter(db.Route.name == RED_LINE_BRAINTREE).first().id

        api_result = API.get("stopsbyroute", {'route': 'Red'})['direction'][0]['stop']
        for item in api_result:

            if item['parent_station_name'] in RED_LINE_BRAINTREE_STATIONS:
                new_station = db.Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                braintree.append(new_station)
            elif item['parent_station_name'] in RED_LINE_ASHMONT_STATIONS:
                new_station = db.Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                ashmont.append(new_station)
            else:
                new_station_ashmont = db.Station(route_id=route_id_ashmont, name_human_readable=item['parent_station_name'],
                                      name_api=item['parent_station'], location_lat=item['stop_lat'],
                                      location_lng=item['stop_lon'])
                new_station_braintree = db.Station(route_id=route_id_braintree, name_human_readable=item['parent_station_name'],
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

                    trips_with_same_id = session.query(db.Trip).filter(db.Trip.api_id == str(trip['trip_id'])).filter(
                        db.Trip.date == datetime.date.today())
                    #print "trips_with_same_id is %s" % trips_with_same_id.count()
                    if trips_with_same_id.count() == 1:
                        # Create a trip record since it exists already

                        new_trip_record = db.TripRecord(trip_id=trips_with_same_id.first().id, location_lat=trip['vehicle']['vehicle_lat'],
                                                     location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.utcnow())

                        to_save.append(new_trip_record)
                    elif trips_with_same_id.count() == 0:
                        if 'Red' in route_name:
                            if string_contains_ashmont_anything(trip['trip_name']):
                                route_name = constants.RED_LINE_ASHMONT
                            elif string_contains_braintree_anything(trip['trip_name']):
                                route_name = constants.RED_LINE_BRAINTREE
                            else:
                                route_name = constants.RED_LINE_ASHMONT

                        route_id = session.query(db.Route).filter(db.Route.name == route_name).first().id

                        station_pair = origin_and_destination_stations(session, trip, route_id)

                        origin_station_id = station_pair[0]
                        destination_station_id = station_pair[1]

                        new_trip = db.Trip(api_id=trip['trip_id'], route_id=route_id, origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                                        date=datetime.datetime.utcnow())

                        session.add(new_trip)
                        session.commit()

                        new_trip_record = db.TripRecord(trip_id=new_trip.id, location_lat=trip['vehicle']['vehicle_lat'],
                                                     location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.utcnow())

                        to_save.append(new_trip_record)

                    else:
                        raise RuntimeError("There were multiple trip objects with the same id: %s" % trips_with_same_id)

    for object in to_save:
        session.merge(object)

    session.commit()

    return to_save

def sync_predictions(routes, session):
    
    Logger.log.info("Syncing predictions...")
    Logger.log.info("Input routes: %s" % routes)

    if 'Red-Ashmont' in routes or 'Red-Braintree' in routes:
        routes.remove('Red-Ashmont')
        routes.remove('Red-Braintree')
        routes.append('Red')

    Logger.log.info("Using routes: %s" % routes)
    
    to_save = []

    route_string = ",".join(routes)
    data = API.get("predictionsbyroutes", {'routes': route_string})
    mode = data['mode']
    for route in mode:
        route_sub = route['route']
        for route_sub_sub in route_sub:
            route_name = route_sub_sub['route_id']
            Logger.log.info("Processing route %s" % route_name)
            for direction in route_sub_sub['direction']:
                for trip in direction['trip']:

                    api_trip_id = trip['trip_id']
                    
                    trip_ref = session.query(db.Trip).filter(db.Trip.api_id == api_trip_id).first()
                    
                    if trip_ref is None:
                        Logger.log.info('No trip record for this prediction. trip_api_id: %s' % api_trip_id)
                        continue
                        
                    for stop in trip['stop']:
                        stop_name = stop['stop_name'].split(' -')[0]
                        
                        if 'JFK/UMASS' in stop_name:
                            stop_name = stop_name.split(' ')[0]
                        
                        try:
                            station_id = session.query(db.Station).filter(db.Station.route_id ==       trip_ref.route_id).filter(db.Station.name_human_readable.like('%' + stop_name + '%')).first().id
                        
                        except AttributeError as e:
                            station_id = station_with_most_similar_name(session, trip_ref.route_id, stop_name)
                            
                        try:
                            seconds = stop['pre_away']
                            
                            
                            new_prediction_record = db.PredictionRecord(trip_id=trip_ref.id, stamp=datetime.datetime.utcnow(),
                                                                  station_id=station_id, seconds_away_from_stop=seconds)

                            to_save.append(new_prediction_record)
                        except KeyError as e:
                            continue
                            Logger.log.info('trip %s has terminated' % api_trip_id)


    for object in to_save:
        session.merge(object)

    session.commit()

    return to_save
