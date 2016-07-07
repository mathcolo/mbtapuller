from geopy.distance import vincenty
from Classes import Station, Trip, TripRecord
import numpy
from geographiclib.geodesic import Geodesic


def find_segment(trip_record, session, test_pair=None):

    if test_pair:
        me_loc = test_pair
    else:
        me_loc = (trip_record.location_lat, trip_record.location_lng)

    all_stations = session.query(Station).all()
    directions = []
    for station in all_stations:
        station_loc = (station.location_lat, station.location_lng)
        directions.append(Geodesic.WGS84.Inverse(me_loc[0],
                                                 me_loc[1],
                                                 station_loc[0],
                                                 station_loc[1])['azi2'])

    direction_reverses = numpy.where(numpy.diff(numpy.sign(directions)))[0]

    return (all_stations[direction_reverses[0]].name_human_readable,all_stations[direction_reverses[0]+1].name_human_readable)
