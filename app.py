from flask import Flask, render_template, request, Response
import json
import requests
import constants

app = Flask(__name__)

valid_routes = [constants.RED_LINE, constants.GREEN_LINE, constants.ORANGE_LINE, constants.BLUE_LINE]

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/getAllTrains", methods=['GET'])
def displayAll():
	trains = [] # replace with array of dicts for each train from backend
	for route in [constants.RED_LINE, constants.GREEN_LINE_B, constants.GREEN_LINE_C, constants.GREEN_LINE_D, 
					constants.GREEN_LINE_E, constants.ORANGE_LINE, constants.BLUE_LINE]:
		trains.append({"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route})
		trains.append({"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route})
	
	js = json.dumps(trains) 

	resp = Response(js, status=200, mimetype='application/json')

	return resp
	
@app.route("/get<string:route>Trains", methods=['GET'])
def getTrainsOnRoute(route):

	if route.lower() not in map(lambda x:x.lower(),valid_routes):
		resp = Response(None, status=404, mimetype='application/json')
	else:
		trains = [
			{"id": route +"-train1", "longitude": 71.0589, "latitude": 42.3601, "route": route},
			{"id": route +"-train2", "longitude": 71.0589, "latitude": 42.3601, "route": route},
			{"id": route +"-train3", "longitude": 71.0589, "latitude": 42.3601, "route": route}
		] # replace with array of dicts for given route from backend
	
		js = json.dumps(trains)

		resp = Response(js, status=200, mimetype='application/json')

	return resp

if __name__ == "__main__":
    app.run()

