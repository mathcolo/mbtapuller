import API
from Classes import Route, Station, Trip
from Miscellaneous import isolate_origin_from_trip_name

def get_stations(route):

    api_result = API.get("stopsbyroute", {'route': route})['direction'][0]['stop']
    stations = []
    for item in api_result:
        new_station = Station(route=1, name_human_readable=item['parent_station_name'], name_api=item['parent_station'], location_lat=item['stop_lat'], location_lng=item['stop_lon'])
        stations.append(new_station)
    return stations


def get_current_trips(routes, session):

    all_trips = []

    route_string = ",".join(routes)
    data = API.get("vehiclesbyroutes", {'routes': route_string})
    mode = data['mode']
    for route in mode:
        route_sub = route['route']
        for direction in route_sub[0]['direction']:
            for trip in direction['trip']:
                # Now we have a trip
                origin_station_id = session.query(Station).filter(
                    Station.name_human_readable.is_(isolate_origin_from_trip_name(trip['trip_name']))).first().id
                destination_station_id = session.query(Station).filter(
                    Station.name_human_readable.is_(trip['trip_headsign'])).first().id

                new_trip = Trip(origin_station_id=origin_station_id, destination_station_id=destination_station_id)
                all_trips.append(new_trip)

    return all_trips
