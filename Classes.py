from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from geopy.distance import vincenty
from constants import *
import Functions

Base = declarative_base()

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)

    route_id = Column(Integer, ForeignKey("routes.id"))
    name_human_readable = Column(String(50))
    name_api = Column(String(50))
    location_lat = Column(Float)
    location_lng = Column(Float)

    def __str__(self):
        return "<Station name=%s on route=%s>" % (self.name_human_readable, self.route_id)

    def __repr__(self):
        return "<Station name=%s on route=%s>" % (self.name_human_readable, self.route_id)

    def loc(self):
        return self.location_lat, self.location_lng


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)

    api_id = Column(String(25))
    date = Column(Date)

    origin_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))

    def __str__(self):
        return "<Trip id=%s from %s to %s>" % (self.id, self.origin_station_id, self.destination_station_id)

    def __repr__(self):
        return "<Trip id=%s from %s to %s>" % (self.id, self.origin_station_id, self.destination_station_id)

    def get_direction(self):
        """
        :return: Returns the trip direction as positive or negative 1, from a database perspective.
        """
        direction = self.destination_station_id > self.origin_station_id
        if direction:
            return 1
        else:
            return -1

    def get_status(self, session):

        most_recent_trip_record = session.query(TripRecord).filter(TripRecord.trip_id == self.id).order_by(
            desc(TripRecord.stamp)).first()

        if most_recent_trip_record is None:
            return STATUS_UNKNOWN, 0

        #print "most_recent_trip_record: %s" % most_recent_trip_record
        #import ipdb; ipdb.set_trace()

        exact_station = most_recent_trip_record.get_exact_station(session)
        if exact_station:
            return STATUS_AT_STATION, exact_station

        # If we get this far, we're not at a station
        # Return what we're between

        return STATUS_IN_TRANSIT, (Functions.find_segment(most_recent_trip_record, session))

class TripRecord(Base):
    __tablename__ = 'triprecords'

    id = Column(Integer, primary_key=True)

    trip_id = Column(Integer, ForeignKey("trips.id"))
    stamp = Column(DateTime)
    location_lat = Column(Float)
    location_lng = Column(Float)

    def __str__(self):
        return "<TripRecord id=%s on trip=%s>" % (self.id, self.trip_id)

    def __repr__(self):
        return "<TripRecord id=%s on trip=%s>" % (self.id, self.trip_id)

    def get_exact_station(self, session):

        all_stations = session.query(Station).all()
        for station in all_stations:
            us = (self.location_lat, self.location_lng)
            it = (station.location_lat, station.location_lng)

            if vincenty(us, it).feet <= 400:
                return station

        return None
