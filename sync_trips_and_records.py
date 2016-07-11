import APIFunctions
import Database
import Classes as c
import vcr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

session = Database.connect()

routes = [x.name for x in session.query(c.Route).all()]

#with vcr.use_cassette('fixtures/vcr_cassettes/sync_trips_and_records.yaml'):
APIFunctions.sync_trips_and_records(routes, session)
