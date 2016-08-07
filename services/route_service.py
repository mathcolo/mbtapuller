from flask import Blueprint, request
import Database
import db_objects as db
import json

route_service = Blueprint('route_service', __name__)

Database.wait_for_available()
session = Database.connect()

@route_service.route("/route", methods=['GET'])
def get_id_for_route():
    id = session.query(db.Route).filter(db.Route.name == request.args['name']).first().id
    return json.dumps(id)