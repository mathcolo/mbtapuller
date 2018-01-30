import db_objects as db
import Database
import datetime

session = Database.connect()

past_bound = datetime.datetime.utcnow() - datetime.timedelta(hours=3)

for trip in session.query(db.Trip).filter(db.Trip.date < past_bound):
    print("{}: {}".format(trip, trip.get_status(session)))
