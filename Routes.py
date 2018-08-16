from constants import *
import db_objects as db

ROUTE_OBJECTS_DICT = {
    RED_LINE: db.Route(name=RED_LINE),
    GREEN_LINE_B: db.Route(name=GREEN_LINE_B),
    GREEN_LINE_C: db.Route(name=GREEN_LINE_C),
    GREEN_LINE_D: db.Route(name=GREEN_LINE_D),
    GREEN_LINE_E: db.Route(name=GREEN_LINE_E),
    BLUE_LINE: db.Route(name=BLUE_LINE),
    ORANGE_LINE: db.Route(name=ORANGE_LINE),
}


def route_names(session):
    return [x.name for x in session.query(db.Route).all()]


def route_ids(session):
    return {x.name: x.id for x in session.query(db.Route).all()}


def get_route_objects():
    return ROUTE_OBJECTS_DICT.values()
