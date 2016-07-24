import time
import argparse
import Logger
import APIFunctions
import Database
import Classes as c


def sync(session, interval=60, once=False):
    while True:
        Logger.log.info('Syncing routes to database')
        routes = list(set([x.name for x in session.query(c.Route).all()]))
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
    sync(session, once=args.once)
