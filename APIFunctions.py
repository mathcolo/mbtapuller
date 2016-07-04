import datetime
import API
from Classes import Station, Trip, TripRecord
from Miscellaneous import isolate_origin_from_trip_name


def get_stations(routes):
    stations = []

    for route in routes:
        api_result = API.get("stopsbyroute", {'route': route})['direction'][0]['stop']
        for item in api_result:
            new_station = Station(route=route, name_human_readable=item['parent_station_name'], name_api=item['parent_station'], location_lat=item['stop_lat'], location_lng=item['stop_lon'])
            stations.append(new_station)
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

                # The MBTA sometimes just throws us random bs
                # Love you guys, but...really?
                if trip['trip_name'] == u'':
                    continue

                # Now we have a trip
                #print "Processing trip_id %s" % trip['trip_id']

                trips_with_same_id = session.query(Trip).filter(Trip.api_id.is_(trip['trip_id'])).filter(
                    Trip.date.is_(datetime.date.today()))
                #print "trips_with_same_id is %s" % trips_with_same_id.count()
                if trips_with_same_id.count() == 1:
                    # Create a trip record since it exists already

                    new_trip_record = TripRecord(trip_id=trips_with_same_id.first().id, location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                    to_save.append(new_trip_record)
                elif trips_with_same_id.count() == 0:

                    origin_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(isolate_origin_from_trip_name(trip['trip_name']))).first().id
                    destination_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(trip['trip_headsign'])).first().id

                    new_trip = Trip(api_id=trip['trip_id'], origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                                    date=datetime.datetime.now())

                    session.add(new_trip)
                    session.commit()

                    new_trip_record = TripRecord(trip_id=new_trip.id, location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'], stamp=datetime.datetime.now())

                    to_save.append(new_trip_record)

                else:
                    raise RuntimeError("There were multiple trip objects with the same id: %s" % trips_with_same_id)

    for object in to_save:
        session.merge(object)

    session.commit()

    return to_save
