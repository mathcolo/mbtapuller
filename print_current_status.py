import db_objects as db
import Database
import datetime

session = Database.connect()

for trip in session.query(db.Trip).filter(db.Trip.date == datetime.datetime.utcnow().date()):
    print "%s: %s" % (trip, trip.get_status(session))
