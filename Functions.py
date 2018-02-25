import datetime
from geopy.distance import vincenty as dist
from sqlalchemy import desc, asc
from sqlalchemy.sql.expression import func
import db_objects as db


def current_trips(session, route_id, time=None):
    if time is None:
        time = datetime.datetime.utcnow()
    five_minutes_ago = time - datetime.timedelta(seconds=300)
    return session.query(db.Trip).filter(db.Trip.stamp_last_seen > five_minutes_ago).filter(
        db.Trip.route_id == int(route_id)).all()


def trip_movement(session, trip, stamp, delta):
    '''
    Answers the question: between stamp and stamp-delta, how far did trip move?
    :param session: The database session to operate with
    :param trip: The trip in question
    :param stamp: A timestamp
    :param delta: A time delta (say, 5 minutes)
    :return: Movement in feet
    '''

    stamp_prev = stamp - delta

    stamp_record = session.query(db.TripRecord)\
                        .filter(db.TripRecord.trip_id == trip.id)\
                        .filter(db.TripRecord.stamp < stamp)\
                        .order_by(db.TripRecord.stamp.desc())\
                        .limit(1)\
                        .first()

    stamp_prev_record = session.query(db.TripRecord)\
                        .filter(db.TripRecord.trip_id == trip.id)\
                        .filter(db.TripRecord.stamp < stamp_prev)\
                        .filter(db.TripRecord.stamp > stamp_prev - datetime.timedelta(minutes=3))\
                        .order_by(db.TripRecord.stamp.desc())\
                        .limit(1)\
                        .first()

    if not stamp_prev_record:
        return -1

    stamp_record_loc = (stamp_record.location_lat, stamp_record.location_lng)
    stamp_prev_record_loc = (stamp_prev_record.location_lat, stamp_prev_record.location_lng)

    return dist(stamp_record_loc, stamp_prev_record_loc).feet


def movement_average_for_stamp(session, stamp):

    trips = current_trips(session, 1)
    print('current_trips length: {}'.format(len(trips)))
    deltas = [trip_movement(session, x, stamp, datetime.timedelta(minutes=6)) for x in
              trips]
    print("deltas before: {}".format(deltas))
    deltas = [x for x in deltas if x > 0.0]
    print("deltas after: {}".format(deltas))
    if len(deltas) == 0:
        return -1
    return sum(deltas) / float(len(deltas))

def current_predictions(session, station_id):
    predictions = session.query(
        db.PredictionRecord.trip_id, db.PredictionRecord.seconds_away_from_stop,
        func.max(db.PredictionRecord.stamp)).filter(db.PredictionRecord.station_id == station_id).group_by(
        db.PredictionRecord.trip_id, db.PredictionRecord.seconds_away_from_stop).order_by(
        func.max(db.PredictionRecord.stamp).desc()).all()

    return predictions


def surrounding_station(session, station):
    '''
    Return surrounding stations for this station

    :param session: The database session to operate with
    :param station: The station in question
    :return: A 2-element tuple containing the forward and backward station
    '''

    max = session.query(db.Station).filter(db.Station.route_id == station.route_id).order_by(
        desc(db.Station.id)).first().id
    min = session.query(db.Station).filter(db.Station.route_id == station.route_id).order_by(
        asc(db.Station.id)).first().id

    plus_id = station.id + 1
    if plus_id > max:
        plus_id = max

    minus_id = station.id - 1
    if minus_id < min:
        minus_id = min

    return (session.query(db.Station).filter(db.Station.id == plus_id).first(),
            session.query(db.Station).filter(db.Station.id == minus_id).first())


def find_segment(trip_record, session, test_pair=None):
    if test_pair:
        me_loc = test_pair
    else:
        me_loc = (trip_record.location_lat, trip_record.location_lng)

    trip = session.query(db.TripRecord, db.Trip).join(db.Trip).filter(db.Trip.id == trip_record.trip_id).first()[1]

    origin_station = session.query(db.Station).filter(db.Station.id == trip.origin_station_id).first()
    destination_station = session.query(db.Station).filter(db.Station.id == trip.destination_station_id).first()

    # print "origin_station: %s" % origin_station
    # print "destination_station: %s" % destination_station

    all_stations = session.query(db.Station).filter(db.Station.route_id == origin_station.route_id).all()
    closest_station = None
    closest_distance_so_far = 100
    for station in all_stations:

        station_loc = (station.location_lat, station.location_lng)
        miles = dist(me_loc, station_loc).miles
        if miles < closest_distance_so_far:
            closest_station = station
            closest_distance_so_far = miles

    surrounding_stations = surrounding_station(session, closest_station)
    surround_station_1 = surrounding_stations[1]
    surround_station_2 = surrounding_stations[0]

    # print("surround_station_1: {}".format(surround_station_1.loc()))
    # print("surround_station_2: {}".format(surround_station_2.loc()))
    if dist(surround_station_1.loc(), destination_station.loc()).miles < dist(surround_station_2.loc(),
                                                                              destination_station.loc()).miles:
        surround_station_ahead = surround_station_1
        surround_station_behind = surround_station_2
    else:
        surround_station_ahead = surround_station_2
        surround_station_behind = surround_station_1

    if dist(me_loc, destination_station.loc()).miles < dist(closest_station.loc(), destination_station.loc()).miles:
        return closest_station, surround_station_ahead
    else:
        return surround_station_behind, closest_station


def all_routes(session):
    routes = session.query(db.Route).all()
    routes_output = []
    for route in routes:
        routes_output.append({'id': route.id, 'name': route.name})

    return routes_output


def get_stations(id, session):
    stations = session.query(db.Station, db.Route).join(db.Route).filter(db.Station.route_id == id).all()

    route_name = session.query(db.Route).filter(db.Route.id == id).one().name

    stations_list = []
    for station in stations:
        stations_list.append(station[0].id)

    return stations_list
