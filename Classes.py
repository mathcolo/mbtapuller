from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from geopy.distance import vincenty

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

    id = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)

    origin_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))

    def get_direction(self):
        """
        :return: Returns the trip direction as ±1, from a database perspective.
        """
        direction = self.destination_station_id > self.origin_station_id
        if direction:
            return 1
        else:
            return -1


class TripRecord(Base):
    __tablename__ = 'triprecords'

    id = Column(Integer, primary_key=True)

    trip_id = Column(String, ForeignKey("trips.id"))
    stamp = Column(DateTime)
    location_lat = Column(Float)
    location_lng = Column(Float)

    def _get_exact_station(self, session):

        all_stations = session.query(Station).all()
        for station in all_stations:
            us = (self.location_lat, self.location_lng)
            it = (station.location_lat, station.location_lng)

            if vincenty(us, it).feet <= 400:
                return station

        return None

    def get_status(self, session):

        #direction is either positive or negative
        associated_trip = session.query(Trip).filter(Trip.id.is_(self.trip_id))

        exact_station = self._get_exact_station(session)
        if exact_station:
            #return ()
            pass
        # If we get this far, we're not at a station


        # (status, station)


        pass