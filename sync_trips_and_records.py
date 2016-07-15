import APIFunctions
import vcr
import Classes as c
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///mbta.db', echo=False)
c.Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

routes = [x.name for x in session.query(c.Route).all()]

#with vcr.use_cassette('fixtures/vcr_cassettes/sync_trips_and_records.yaml'):
APIFunctions.sync_trips_and_records(routes, session)
