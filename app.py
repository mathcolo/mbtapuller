from initial_setup import initial_setup
from flask import Flask, render_template, request, Response
import json
import requests
import constants
import Database
import Functions
import db_objects as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Database.wait_for_available()
session = Database.connect()
if not Database.is_setup(session):
	initial_setup()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	lines = sorted(getAllRoutes(), key=lambda k: k['name']) 
	
	return render_template('index.html', lines=lines)

@app.route("/trains", methods=['GET'])
def display_all():
	trains = [] # replace with array of dicts for each train from backend
	for route in [constants.RED_LINE_ASHMONT, constants.RED_LINE_BRAINTREE, constants.GREEN_LINE_B, constants.GREEN_LINE_C, constants.GREEN_LINE_D, 
					constants.GREEN_LINE_E, constants.ORANGE_LINE, constants.BLUE_LINE]:
		trains.append({"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route})
	
	return json.dumps(trains)
	
@app.route("/trains/<string:route>", methods=['GET'])
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
	
@app.route("/stations/all", methods=['GET'])
def get_all_stations():
	stations = []
	for route in valid_routes:
		stations.append(Functions.get_stations(route, session))
	
	return json.dumps(stations)

	
@app.route("/stations/<string:route_id>", methods=['GET'])
def get_stations_on_route(route_id):
	stations = Functions.get_stations(route_id, session)
	return json.dumps(stations)

@app.route("/routes", methods=['GET'])
def get_all_routes():
	return Functions.all_routes(session)

@app.route("/id", methods=['GET'])
def get_id_for_route():
	id = session.query(db.Route).filter(db.Route.name == name).one().id
	return json.dumps(id)
	
@app.route("/station/<string:station_id>", methods=['GET'])
def get_station_details(station_id):
    station = session.query(db.Station).filter(db.Station.id == station_id).one()
	
	route_name = session.query(db.Route).filter(db.Route.id == station.route_id).one().name
	
	stations_details = {'name': station.name_human_readable, 'route_name': route_name, 'id': station.id}
	return json.dumps(stations_details)

if __name__ == "__main__":
    app.run()

