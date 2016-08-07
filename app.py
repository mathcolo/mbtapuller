from initial_setup import initial_setup
from flask import Flask, render_template
import Database
import Functions

from services.stations_service import stations_service
from services.station_details_service import station_details_service
from services.train_service import train_service
from services.route_service import route_service

Database.wait_for_available()
session = Database.connect()
if not Database.is_setup(session):
	initial_setup()

app = Flask(__name__)

app.register_blueprint(stations_service)
app.register_blueprint(station_details_service)
app.register_blueprint(train_service)
app.register_blueprint(route_service)

@app.route("/", methods=['GET', 'POST'])
def home():
	lines = sorted(Functions.all_routes(session), key=lambda k: k['name']) 
	
	return render_template('index.html', lines=lines)

if __name__ == "__main__":
	app.run()
