import argparse
import APIFunctions
import vcr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Classes import Base, Trip, Station, TripRecord

parser = argparse.ArgumentParser()
parser.add_argument("routes", help="The routes you want to capture in MBTA v2 format-- example: Red,Green-D,Orange")
args = vars(parser.parse_args())
routes = args['routes'].split(',')

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

#with vcr.use_cassette('fixtures/vcr_cassettes/sync_trips_and_records.yaml'):
APIFunctions.sync_trips_and_records(routes, session)
