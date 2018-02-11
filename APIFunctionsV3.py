import Logger
import datetime
import API
import db_objects as db
from utilities import *
from constants import *


def get_routes():
    routes = [
        db.Route(name=RED_LINE),
        # db.Route(name=GREEN_LINE_B),
        # db.Route(name=GREEN_LINE_C),
        # db.Route(name=GREEN_LINE_D),
        # db.Route(name=GREEN_LINE_E),
        # db.Route(name=BLUE_LINE),
        # db.Route(name=ORANGE_LINE),
    ]
    return routes


def get_stations(session):

    new_stations = []
    routes = session.query(db.Route).all()

    for route in routes:
        station_data = API.getV3('stops', 'route', route.name)

        for station in station_data['data']:
            new_station = db.Station(route_id=route.name,
                                     name_human_readable=station['attributes']['name'],
                                     name_api=station['id'],
                                     location_lat=station['attributes']['latitude'],
                                     accessible=station['attributes']['wheelchair_boarding'],
                                     location_lng=station['attributes']['longitude'])
            new_stations.append(new_station)

    return new_stations


def sync_trips_and_records(routes, session):

    Logger.log.info('Syncing trips...')
    Logger.log.info('Input routes: %s' % routes)

    to_save = []

    for route in routes:
        vehicles = API.getV3('vehicles', 'route', route)['data']
        for vehicle in vehicles:
            vehicle_route = vehicle['relationships']['route']['data']

            vehicle_trip = vehicle['relationships']['trip']['data']
            vehicle_trip_id = vehicle_trip['id']
            vehicle_lat = vehicle['attributes']['latitude']
            vehicle_lon = vehicle['attributes']['longitude']

            trips_with_same_id = session.query(db.Trip).filter(db.Trip.api_id == vehicle_trip_id).filter(
                            db.Trip.date == datetime.datetime.utcnow().date())

            if trips_with_same_id.count() == 1:

                new_trip_record = db.TripRecord(trip_id=trips_with_same_id.first().id,
                                                location_lat=vehicle_lat,
                                                location_lng=vehicle_lon,
                                                stamp=datetime.datetime.utcnow())

                to_save.append(new_trip_record)

                # Update the trip's last seen time
                session.query(db.Trip).filter(db.Trip.id == trips_with_same_id.first().id) \
                    .update({'stamp_last_seen': datetime.datetime.utcnow()})

            elif trips_with_same_id.count() == 0:
                route_id = session.query(db.Route).filter(db.Route.name == route).first().id

                new_trip = db.Trip(api_id=vehicle_trip_id,
                                   route_id=route_id,
                                   direction_id=vehicle['attributes']['direction_id'],
                                   lead=vehicle['attributes']['label'],
                                   date=datetime.datetime.utcnow(),
                                   stamp_first_seen=datetime.datetime.utcnow(),
                                   stamp_last_seen=datetime.datetime.utcnow())

                session.add(new_trip)
                session.commit()

                new_trip_record = db.TripRecord(trip_id=new_trip.id,
                                                location_lat=vehicle_lat,
                                                location_lng=vehicle_lon,
                                                stamp=datetime.datetime.utcnow())

                to_save.append(new_trip_record)

    for object in to_save:
        session.merge(object)

    session.commit()


if __name__ == '__main__':
    import Database
    session = Database.connect()
    sync_trips_and_records(get_routes(), session)