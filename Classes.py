from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from geopy.distance import vincenty
from constants import *

Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)

    route = Column(String)
    name_human_readable = Column(String)
    name_api = Column(String)
    location_lat = Column(Float)
    location_lng = Column(Float)


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)

    api_id = Column(String)
    date = Column(Date)

    origin_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))

    def get_direction(self):
        """
        :return: Returns the trip direction as positive or negative 1, from a database perspective.
        """
        direction = self.destination_station_id > self.origin_station_id
        if direction:
            return 1
        else:
            return -1

    def get_last_station(self, session):

        all_trip_records = session.query(TripRecord).filter(TripRecord.trip_id.is_(self.id)).order_by(desc(TripRecord.stamp)).all()

        potential_station = None
        print "all_trip_records: %s" % all_trip_records
        for trip_record in all_trip_records:
            print "checking trip record %s" % trip_record.trip_id
            potential_station = trip_record.get_exact_station(session)
            print "potential_station human readable name: %s" % potential_station.name_human_readable
            if potential_station:
                return potential_station

        assert potential_station is not None
        return potential_station


class TripRecord(Base):
    __tablename__ = 'triprecords'

    id = Column(Integer, primary_key=True)

    trip_id = Column(String, ForeignKey("trips.id"))
    stamp = Column(DateTime)
    location_lat = Column(Float)
    location_lng = Column(Float)

    def get_exact_station(self, session):

        all_stations = session.query(Station).all()
        for station in all_stations:
            us = (self.location_lat, self.location_lng)
            it = (station.location_lat, station.location_lng)

            if vincenty(us, it).feet <= 400:
                return station

        return None

    def get_status(self, session):

        #direction is either positive or negative
        associated_trip = session.query(Trip).filter(Trip.id.is_(self.trip_id)).first()

        exact_station = self.get_exact_station(session)
        if exact_station:
            return STATUS_AT_STATION, exact_station

        # If we get this far, we're not at a station
        # Find the next station

        last_station = associated_trip.get_last_station(session)

        next_station_in_theory_id = last_station.id + self.get_direction()
        my_route = session.query(Station).filter(Station.id.is_(self.origin_station_id)).first()
        next_station_in_theory = session.query(Station).filter(Station.id.is_(next_station_in_theory_id)).first()
        if my_route.name_api != next_station_in_theory.name_api:
            return None

        return STATUS_IN_TRANSIT, next_station_in_theory