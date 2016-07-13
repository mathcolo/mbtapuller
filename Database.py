from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Classes as c
import os
import time
import socket

def wait_for_available(host='db', port=3306, interval=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_check = sock.connect_ex((host, port))

    while True:
        if port_check == 0:
            return
        else:
            print "Database isn't up yet, sleeping for %s seconds" % interval
            time.sleep(interval)


def connect(create_all=False, use_mysql=False):

    if 'USE_MYSQL' in os.environ or use_mysql:
        db = create_engine('mysql://mbtapuller:mbtapuller@db/mbtapuller', echo=False)
    else:
        db = create_engine('sqlite:///mbta.db', echo=False)

    if create_all:
        c.Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    session = Session()

    return session