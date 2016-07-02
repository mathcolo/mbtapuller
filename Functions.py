from geopy.distance import vincenty
from Classes import Station

def current_station(trip_record, session):

    all_stations = session.query(Station).all()
    for station in all_stations:
        us = (trip_record.location_lat, trip_record.location_lng)
        it = (station.location_lat, station.location_lng)

        if vincenty(us,it).feet <= 400:
            return station

    return None
