from flask import Blueprint
import Functions
import Database
import db_objects as db
from sqlalchemy import asc, desc
import json

stations_service = Blueprint('stations_service', __name__)

Database.wait_for_available()
session = Database.connect()

@stations_service.route("/stations/<string:route_id>", methods=['GET'])
def get_stations_on_route(route_id):
    stations = Functions.get_stations(route_id, session)
    return json.dumps(stations)

@stations_service.route("/stations/<string:route_id>/terminal", methods=['GET'])
def get_terminal_stations(route_id):
    first = session.query(db.Station).filter(db.Station.route_id == route_id).order_by(asc(db.Station.id)).limit(1).first()
    last = session.query(db.Station).filter(db.Station.route_id == route_id).order_by(desc(db.Station.id)).limit(1).first()

    return json.dumps({'first': first.name_human_readable, 'last': last.name_human_readable})