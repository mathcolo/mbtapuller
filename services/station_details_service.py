from flask import Blueprint
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
	predictions = Functions.current_predictions(session, station_id)
	
	directed_predictions = []
    
	if (predictions is not None):
		for prediction in predictions:
			trip = session.query(db.Trip).filter(db.Trip.id == prediction.trip_id).first()
			dir = int(trip.destination_station_id > trip.origin_station_id)
            
			if (int(direction) is dir):
				directed_predictions.append(prediction)
		
		if len(directed_predictions) == 0:
			return json.dumps({'prediction1': None, 'prediction2' : None})
				
		directed_predictions.sort(key=lambda x: x.seconds_away_from_stop)
		
		if len(directed_predictions) > 1:
			next_two_pre = {'prediction1': directed_predictions[0].seconds_away_from_stop, 'prediction2' : directed_predictions[1].seconds_away_from_stop}
			
		else:
			next_two_pre = {'prediction1': directed_predictions[0].seconds_away_from_stop, 'prediction2' : None}
			
		return json.dumps(next_two_pre)
	else:
		return json.dumps({'prediction1': None, 'prediction2' : None})