import APIFunctions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Classes

db = create_engine('sqlite:///mbta.db', echo=False)
Classes.Base.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()



# red_stations = APIFunctions.get_stations('Red')
# for station in red_stations:
#     session.add(station)
#
# session.commit()

print session.query(Classes.Station).filter(Classes.Station.name_human_readable.is_('Alewife')).first().location_lat

all_red_trips = APIFunctions.get_current_trips(['Red'], session)

for trip in all_red_trips:
    print trip