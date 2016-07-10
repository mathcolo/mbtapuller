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
	lines = sorted(getAllRoutes(), key=lambda k: k['name']) 
	
	return render_template('index.html', lines=lines)
	
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
	
@app.route("/stations/<string:route_id>", methods=['GET'])
def getStationsOnRoute(route_id):
	stations = Functions.get_stations(route_id, session)
	
	js = json.dumps(stations)

	resp = Response(js, status=200, mimetype='application/json')

	return resp

@app.route("/routes", methods=['GET'])
def getAllRoutes():
	routes = Functions.all_routes(session)

	return routes

if __name__ == "__main__":
    app.run()

