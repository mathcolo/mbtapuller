from initial_setup import initial_setup
from flask import Flask, render_template, request, Response
import json
import requests
import constants
import Database
import Functions
from Classes import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# db = create_engine('sqlite:///mbta.db', echo=False)
# Base.metadata.create_all(db)
# Session = sessionmaker(bind=db)
# session = Session()
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
def displayAll():
	trains = [] # replace with array of dicts for each train from backend
	for route in [constants.RED_LINE_ASHMONT, constants.RED_LINE_BRAINTREE, constants.GREEN_LINE_B, constants.GREEN_LINE_C, constants.GREEN_LINE_D, 
					constants.GREEN_LINE_E, constants.ORANGE_LINE, constants.BLUE_LINE]:
		trains.append({"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route})
	
	return json.dumps(trains)
	
@app.route("/trains/<string:route>", methods=['GET'])
def getTrainsOnRoute(route):

	trains = [
		{"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route},
		{"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route},
		{"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route}
	] # replace with array of dicts for given route from backend

	return json.dumps(trains)
	
@app.route("/stations/all", methods=['GET'])
def getAllStations():
	stations = []
	for route in valid_routes:
		stations.append(Functions.get_stations(route, session))
	
	return json.dumps(stations)

	
@app.route("/stations/<string:route_id>", methods=['GET'])
def getStationsOnRoute(route_id):
	stations = Functions.get_stations(route_id, session)
	return json.dumps(stations)

@app.route("/routes", methods=['GET'])
def getAllRoutes():
	return Functions.all_routes(session)

@app.route("/id", methods=['GET'])
def getIdForRoute():
	id = Functions.getIdForRoute(request.args['name'], session)
	return json.dumps(id)

if __name__ == "__main__":
    app.run()

