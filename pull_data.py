import time
import argparse
import Logger
import datetime
import APIFunctions
import Database
import db_objects as db


def pull(session, interval=60, once=False):
    while True:
        now = datetime.datetime.now()
        if 1 <= now.hour <= 5:
            Logger.log.info('Skipping sync, time is between 1 and 6AM')
        else:
            Logger.log.info('Syncing routes to database')
            routes = [x.name for x in session.query(db.Route).all()]
            APIFunctions.sync_trips_and_records(routes, session)
            APIFunctions.sync_predictions(routes, session)
            if once:
                break
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", help="sync once; don't loop", action='store_true')
    args = parser.parse_args()

    session = Database.connect()
    pull(session, once=args.once)
