import sys
import APIFunctions
import Database
import Logger
import db_objects as db

def initial_setup():
    Database.wait_for_available()

    # Make a database connection
    session = Database.connect(create_all=True)

    if session.query(db.Route).count() > 0 or session.query(db.Station).count() > 0:
        Logger.log.error("ERROR: Initial setup cannot continue, this database already has route and station data.")
        sys.exit(1)

    routes = APIFunctions.get_routes()
    for route in routes:
        session.add(route)

    # Get the station objects and add them to the database
    stations = APIFunctions.get_stations(session)
    for station in stations:
        session.add(station)

    session.commit()

if __name__ == '__main__':
    initial_setup()
