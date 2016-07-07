from geopy.distance import vincenty as dist
from Classes import Station, Trip, TripRecord


def find_segment(trip_record, session, test_pair=None):

    if test_pair:
        me_loc = test_pair
    else:
        me_loc = (trip_record.location_lat, trip_record.location_lng)


    destination_station = session.query(Station).filter(Station.id == 1).first()

    all_stations = session.query(Station).all()
    closest_station = None
    closest_distance_so_far = 100
    for station in all_stations:

        # Red Line override
        if destination_station.name_human_readable == 'Braintree':
            if station.name_human_readable in ['Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont']:
                continue

        if destination_station.name_human_readable == 'Ashmont':
            if station.name_human_readable in ['North Quincy', 'Wollaston', 'Quincy Center', 'Quincy Adams', 'Braintree']:
                continue

        station_loc = (station.location_lat, station.location_lng)
        miles = dist(me_loc, station_loc).miles
        if miles < closest_distance_so_far:
            closest_station = station
            closest_distance_so_far = miles

    surround_station_1 = session.query(Station).filter(Station.id == closest_station.id+1).first()
    surround_station_2 = session.query(Station).filter(Station.id == closest_station.id-1).first()

    if dist(surround_station_1.loc(), destination_station.loc()) < dist(surround_station_2.loc(), destination_station.loc()):
        surround_station_ahead = surround_station_1
        surround_station_behind = surround_station_2
    else:
        surround_station_ahead = surround_station_2
        surround_station_behind = surround_station_1

    if dist(me_loc, destination_station.loc()) < dist(closest_station.loc(), destination_station.loc()):
        return closest_station.name_human_readable, surround_station_ahead.name_human_readable
    else:
        return surround_station_behind.name_human_readable, closest_station.name_human_readable