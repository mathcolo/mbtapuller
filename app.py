from flask import Flask, render_template, request, Response
import json
import requests
import constants
import Functions
from Classes import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route("/getAllTrains", methods=['GET'])
def displayAll():
	trains = [] # replace with array of dicts for each train from backend
	for route in [constants.RED_LINE_ASHMONT, constants.RED_LINE_BRAINTREE, constants.GREEN_LINE_B, constants.GREEN_LINE_C, constants.GREEN_LINE_D, 
					constants.GREEN_LINE_E, constants.ORANGE_LINE, constants.BLUE_LINE]:
		trains.append({"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route})
	
	js = json.dumps(trains) 

	resp = Response(js, status=200, mimetype='application/json')

	return resp
	
@app.route("/get<string:route>Trains", methods=['GET'])
def getTrainsOnRoute(route):

	trains = [
		{"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route},
		{"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route},
		{"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route}
	] # replace with array of dicts for given route from backend

	js = json.dumps(trains)

	resp = Response(js, status=200, mimetype='application/json')

	return resp
	
@app.route("/stations/all", methods=['GET'])
def getAllStations():
	
	stations = []
	
	for route in valid_routes:
		stations.append(Functions.get_stations(route, session))
	
	js = json.dumps(stations)

	resp = Response(js, status=200, mimetype='application/json')

	return resp
	
@app.route("/stations/<string:route_id>", methods=['GET'])
def getStationsOnRoute(route_id):
	stations = Functions.get_stations(route_id, session)
	
	js = json.dumps(stations)

	resp = Response(js, status=200, mimetype='application/json')

	return resp

@app.route("/routes", methods=['GET'])
def getAllRoutes():
	return json.dumps(Functions.all_routes(session))


if __name__ == "__main__":
    app.run()

