import APIFunctions
import Database


def initial_setup():
    Database.wait_for_available()

    # Make a database connection
    session = Database.connect(create_all=True)

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
