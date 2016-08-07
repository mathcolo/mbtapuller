from flask import Blueprint
import Functions
import Database
import json

train_service = Blueprint('train_service', __name__)

Database.wait_for_available()
session = Database.connect()

@train_service.route("/trains/<string:route>", methods=['GET'])
def get_trains_on_route(route):

    trips = Functions.current_trips(session, route)
    response_objects = []

    for trip in trips:
        status = trip.get_status(session)
        direction = int(trip.destination_station_id > trip.origin_station_id)
        output = {
            'id': trip.id,
            'status': status[0],
            'destination': trip.destination_station_id,
            'direction': direction,
            'station_1': None,
            'station_2': None,
        }
        if output['status'] == 'IN_TRANSIT':
            output['station_1'] = status[1][0].name_human_readable
            output['station_2'] = status[1][1].name_human_readable
        elif output['status'] == 'AT_STATION':
            output['station_1'] = status[1].name_human_readable
        response_objects.append(output)

    return json.dumps(response_objects)