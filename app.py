from flask import Flask, render_template, make_response, jsonify, send_from_directory
import Database
import Functions
import StatCache
import StatPlot

from services.stations_service import stations_service
from services.station_details_service import station_details_service
from services.train_service import train_service
from services.route_service import route_service

Database.wait_for_available()
session = Database.connect()

app = Flask(__name__)

app.register_blueprint(stations_service)
app.register_blueprint(station_details_service)
app.register_blueprint(train_service)
app.register_blueprint(route_service)


@app.route("/", methods=['GET', 'POST'])
def home():
    lines = sorted(Functions.all_routes(session), key=lambda k: k['name'])
    return render_template('index.html', lines=lines)


@app.route("/stat")
def stat():
    plot = make_response(StatPlot.stat_figure('movement_average').getvalue())
    plot.mimetype = 'image/png'
    return plot


@app.route("/stat.json")
def stat_json():
    return jsonify(StatCache.circular_all(Database.connect_redis(), 'movement_average')[::-1])


@app.route("/viewer/")
def stat_modern():
    return send_from_directory('static-npm/dist/', 'index.html')


@app.route("/viewer/bundle.js")
def stat_modern_js():
    return send_from_directory('static-npm/dist/', 'bundle.js')


if __name__ == "__main__":
    app.run()
