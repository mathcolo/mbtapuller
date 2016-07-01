import APIFunctions
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Classes import Base, Trip, Station, TripRecord

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()



red_stations = APIFunctions.get_stations('Red')
for station in red_stations:
    session.add(station)

session.add(Trip(id=1, date=datetime.datetime.now(), origin_station_id=3, destination_station_id=4))

session.commit()