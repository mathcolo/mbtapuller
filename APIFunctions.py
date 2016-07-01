import datetime
import API
from Classes import Station, Trip, TripRecord
from Miscellaneous import isolate_origin_from_trip_name

def get_stations(route):

    api_result = API.get("stopsbyroute", {'route': route})['direction'][0]['stop']
    stations = []
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
                # Now we have a trip
                print "Processing trip_id %s" % trip['trip_id']

                trips_with_same_id = session.query(Trip).filter(Trip.id.is_(trip['trip_id'])).count()
                if trips_with_same_id == 1:
                    # Create a trip record since it exists already

                    new_trip_record = TripRecord(trip_id=trip['trip_id'], location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'])

                    to_save.append(new_trip_record)
                elif trips_with_same_id == 0:

                    origin_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(isolate_origin_from_trip_name(trip['trip_name']))).first().id
                    destination_station_id = session.query(Station).filter(
                        Station.name_human_readable.is_(trip['trip_headsign'])).first().id

                    new_trip = Trip(id=trip['trip_id'], origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                                    date=datetime.datetime.now())

                    new_trip_record = TripRecord(trip_id=trip['trip_id'], location_lat=trip['vehicle']['vehicle_lat'],
                                                 location_lng=trip['vehicle']['vehicle_lon'])

                    to_save.append(new_trip)
                    to_save.append(new_trip_record)

                else:
                    raise RuntimeError("There were multiple trip objects with the same id: %s" % trips_with_same_id)

    for object in to_save:
        session.merge(object)

    return to_save
