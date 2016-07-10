from Classes import Base, Trip
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

for trip in session.query(Trip).all():
  print "%s: %s" % (trip, trip.get_status(session))
