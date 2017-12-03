import time
import argparse
import Logger
import datetime
import APIFunctions
import Database
import pytz
import traceback
import db_objects as db
from initial_setup import initial_setup


def pull(session, interval=60, once=False):
    while True:
        # This is timezone specific because the train schedule itself operates on ET, not UTC!
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))

        if 1 <= now.hour <= 5:
            Logger.log.info('Skipping sync, time is between 1 and 6AM')
        else:
            Logger.log.info('Syncing routes to database')
            routes = [x.name for x in session.query(db.Route).all()]
            try:
                pass
                APIFunctions.sync_trips_and_records(routes, session)
                # APIFunctions.sync_predictions(routes, session)
            except Exception as e:
                Logger.log.error('ERROR: Data pull failed, retrying in {} seconds'.format(interval))
                traceback.print_exc()

            if once:
                break
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", help="sync once; don't loop", action='store_true')
    args = parser.parse_args()

    Database.wait_for_available()
    session = Database.connect()
    if not Database.is_setup(session):
        initial_setup()

    pull(session, once=args.once)
