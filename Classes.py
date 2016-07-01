from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

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

    date = Column(Date)
    origin_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))


class TripRecord(Base):
    __tablename__ = 'triprecords'

    id = Column(Integer, primary_key=True)

    trip_id = Column(String, ForeignKey("trips.id"))
    location_lat = Column(Float)
    location_lng = Column(Float)
