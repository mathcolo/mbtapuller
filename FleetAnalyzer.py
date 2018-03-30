import datetime
import pytz
import db_objects as db
import Database
from constants import *


def todays_vehicles_for_route(session, route_id):
    lower_bound_date = pytz.timezone('America/New_York').localize(datetime.datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
    upper_bound_date = datetime.datetime.utcnow()
    print([x.lead for x in session.query(db.Trip).filter(db.Trip.route_id == route_id).filter(db.Trip.stamp_first_seen > lower_bound_date).filter(db.Trip.stamp_last_seen < upper_bound_date).all()])
    pass


vehicle_type_map(Database.connect(), 1)
