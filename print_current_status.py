import db_objects as db
import Database
import datetime
import Functions


def movement_average_for_stamp(session, stamp):

    current_trips = Functions.current_trips(session, 1)
    deltas = [Functions.trip_movement(session, x, stamp, datetime.timedelta(minutes=6)) for x in
              current_trips]
    deltas = [x for x in deltas if x != -1]
    return sum(deltas) / float(len(deltas))


def last_n_minutes(session, minutes=30):

    averages = []
    current_time = datetime.datetime.utcnow()
    while current_time > datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes):
        averages.append(movement_average_for_stamp(session, current_time))
        current_time = current_time - datetime.timedelta(minutes=6)
    return averages


session = Database.connect()
print(movement_average_for_stamp(session, datetime.datetime.utcnow()))
# print(last_n_minutes(session))

