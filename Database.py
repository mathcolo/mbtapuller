import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Classes as c
import os
import time
import socket

DB_HOST = 'db_1'
DB_PORT = 3306
DB_USER = 'mbtapuller'
DB_PASSWORD = 'mbtapuller'
DB_NAME = 'mbtapuller'


def wait_for_available(host=DB_HOST, port=DB_PORT, interval=5):
    time.sleep(interval)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_check = sock.connect_ex((host, port))

    while True:
        if port_check == 0:
            return
        else:
            print "Database isn't available, sleeping for %s seconds" % interval
            time.sleep(interval)


def connect(create_all=False, use_mysql=False):

    Logger.log.info('Connecting to database')

    if 'USE_MYSQL' in os.environ or use_mysql:
        Logger.log.info('Using MySQL server %s' % DB_HOST)
        db = create_engine('mysql://%s:%s@%s:%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME), echo=False)
    else:
        Logger.log.info('Using SQLite')
        db = create_engine('sqlite:///mbta.db', echo=False)

    if create_all:
        c.Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    session = Session()

    return session


def is_setup(session):
    try:
        num_routes = session.query(c.Route).count()

        if num_routes > 0:
            return True
        else:
            return False
    except:
        return False
