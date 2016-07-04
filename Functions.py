from geopy.distance import vincenty
from Classes import Station
import constants
import pdb
import argparse
from Classes import *
import APIFunctions
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_

db = create_engine('sqlite:///mbta.db', echo=False)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()


def current_station(trip_record, session):
    """
    Find the current station that a TripRecord is at.

    Example return: Harvard station object, Alewife station object
    Example if the train is not within 400 of a station: None

    :param trip_record: The TripRecord object to evaluate.
    :param session: The database session to use for data queries
    :return: A Station object
    """
    all_stations = session.query(Station).all()
    for station in all_stations:
        us = (trip_record.location_lat, trip_record.location_lng)
        it = (station.location_lat, station.location_lng)

        if vincenty(us, it).feet <= 400:
            return station

    return None
	
def get_stations(route, session):
	if route.lower() == constants.RED_LINE.lower():
	
		start_id = session.query(Station).filter(Station.name_api == 'place-alfcl').one().id
		
		print(start_id)
	
		braintree = session.query(Station).filter(Station.route == route.title()).filter(or_(Station.id > start_id + 17, Station.id < start_id + 13)).order_by(Station.id).all()
		ashmont = session.query(Station).filter(Station.route == route.title()).filter(Station.id < start_id + 17).all()
		
		for b in braintree:
			print b.name_human_readable
		
		return [braintree, ashmont]
		
	elif route.lower() == constants.GREEN_LINE.lower():

		b = session.query(Station).filter(Station.route == constants.GREEN_LINE_B).all()
		c = session.query(Station).filter(Station.route == constants.GREEN_LINE_C).all()
		d = session.query(Station).filter(Station.route == constants.GREEN_LINE_D).all()
		e = session.query(Station).filter(Station.route == constants.GREEN_LINE_E).all()
		
		stations = [b, c, d, e]
			
		return stations
	
	elif route.lower() in [constants.ORANGE_LINE.lower(), constants.BLUE_LINE.lower()]:
		stations = session.query(Station).filter(Station.route == route.title()).all()

		return stations
		
	return None
	
get_stations('red', session)