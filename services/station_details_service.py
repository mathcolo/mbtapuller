from flask import Blueprint
import datetime
import Functions
import Database
import db_objects as db
import json

station_details_service = Blueprint('station_details_service', __name__)

Database.wait_for_available()
session = Database.connect()

@station_details_service.route("/station/<string:station_id>", methods=['GET'])
def get_station_details(station_id):
    station = session.query(db.Station).filter(db.Station.id == station_id).one()
    route_name = session.query(db.Route).filter(db.Route.id == station.route_id).one().name

    out_predictions = json.loads(get_next_service_for_station(station_id, False))
    in_predictions = json.loads(get_next_service_for_station(station_id, True))

    stations_details = {'name': station.name_human_readable,
                        'route_name': route_name,
                        'id': station.id,
                       'outbound_pre' : {'pre_1' : out_predictions['prediction1'], 'pre_2' : out_predictions['prediction2']},
                        'inbound_pre' : {'pre_1' : in_predictions['prediction1'],'pre_2' : in_predictions['prediction2']}
                       }

    return json.dumps(stations_details)

@station_details_service.route("/station/<string:station_id>/direction/<string:direction>/details", methods=['GET'])
def get_directed_station_details(station_id, direction):
    station = session.query(db.Station).filter(db.Station.id == station_id).one()
    route_name = session.query(db.Route).filter(db.Route.id == station.route_id).one().name

    predictions = json.loads(get_next_service_for_station(station_id, direction))

    stations_details = {'name': station.name_human_readable,
                        'route_name': route_name,
                        'id': station.id,
                       'pre_1': predictions['prediction1'],
                       'pre_2': predictions['prediction2']}

    return json.dumps(stations_details)

@station_details_service.route("/station/<string:station_id>/direction/<string:direction>/nextservice", methods=['GET'])
def get_next_service_for_station(station_id, direction):
    most_recent_pull_time = session.query(db.PredictionRecord).order_by(db.PredictionRecord.stamp.desc()).limit(
        1).first().stamp
    most_recent_pull_time_threshold = most_recent_pull_time - datetime.timedelta(seconds=5)

    # Time since that most recent pull ^
    time_since_pull = int((datetime.datetime.utcnow() - most_recent_pull_time).total_seconds())

    lowest_to_station = None
    second_lowest_to_station = None

    prediction_records = (
        session.query(db.PredictionRecord)
            .filter(db.PredictionRecord.station_id == station_id)
            .filter(db.PredictionRecord.trip_direction == direction)
            .filter(db.PredictionRecord.stamp > most_recent_pull_time_threshold)
            .order_by(db.PredictionRecord.seconds_away_from_stop)
            .all()
    )

    if len(prediction_records) > 0:
        lowest_to_station = prediction_records[0].seconds_away_from_stop

    if len(prediction_records) > 1:
        second_lowest_to_station = prediction_records[1].seconds_away_from_stop

    return json.dumps({'prediction1': lowest_to_station,
                       'prediction2': second_lowest_to_station,
                       'age': time_since_pull,
                       })
