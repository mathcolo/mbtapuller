import Classes as c
import Database
import datetime

session = Database.connect()

for trip in session.query(c.Trip).filter(c.Trip.date == datetime.date.today()):
    print "%s: %s" % (trip, trip.get_status(session))
