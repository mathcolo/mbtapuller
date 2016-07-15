import time
import Logger
import APIFunctions
import Database
import Classes as c
import vcr

def sync(session, interval=60):
    while True:
        time.sleep(interval)

        Logger.log.info('Syncing routes to database')
        routes = [x.name for x in session.query(c.Route).all()]

        #with vcr.use_cassette('fixtures/vcr_cassettes/sync_trips_and_records.yaml'):
        APIFunctions.sync_trips_and_records(routes, session)

if __name__ == '__main__':
    session = Database.connect()
    sync(session)