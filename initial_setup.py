import APIFunctions
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Classes import Base

parser = argparse.ArgumentParser()
parser.add_argument("routes", help="The routes you want to capture in MBTA v2 format-- example: Red,Green-D,Orange")
args = vars(parser.parse_args())
routes = args['routes'].split(',')

# Make a database connection
db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

routes = APIFunctions.get_routes()
for route in routes:
    session.add(route)

# Get the station objects and add them to the database
stations = APIFunctions.get_stations(session)
for station in stations:
    session.add(station)

session.commit()