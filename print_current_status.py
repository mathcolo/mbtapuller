import Classes as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import Database

session = Database.connect()

for trip in session.query(c.Trip).all():
    print "%s: %s" % (trip, trip.get_status(session))
