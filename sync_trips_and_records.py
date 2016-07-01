import argparse
import APIFunctions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Classes import Base, Trip, Station, TripRecord

# parser = argparse.ArgumentParser()
#
# parser.add_argument("routes", help="The routes you want to capture in MBTA v2 format-- example: Red,Green-D,Orange")
# parser.add_argument("db", help="Database connection")
# parser.parse_args()

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

APIFunctions.sync_trips_and_records(['Red'], session)

session.commit()
