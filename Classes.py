from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import geopy

Base = declarative_base()

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    route = Column(Integer)

    name_human_readable = Column(String)
    name_api = Column(String)

    location_lat = Column(Float)
    location_lng = Column(Float)


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(String, primary_key=True)

    origin_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))



    location_lat = Column(Float)
    location_lng = Column(Float)

# TRIP SHOULD BECOME TRIP AND TRIPSTATE