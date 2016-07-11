from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Classes as c
import os

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