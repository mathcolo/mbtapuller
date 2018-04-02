import datetime
import pytz
import db_objects as db
import Routes
from constants import *
from collections import Counter


def todays_vehicles_for_route(session, route_id):
    """
    :param route_id: The route name
    :return: The deduped list of vehicles we've seen between 3AM local time, and the current time
    """
    lower_bound_date = pytz.timezone('America/New_York').localize(
        datetime.datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
    upper_bound_date = datetime.datetime.utcnow()

    return prune_lead_list([x.lead for x in session.query(db.Trip.lead).filter(db.Trip.route_id == route_id).filter(
        db.Trip.stamp_first_seen > lower_bound_date).filter(db.Trip.stamp_last_seen < upper_bound_date).distinct()])


def model_frequency_for_route(session, route_name):
    return model_frequency(todays_vehicles_for_route(session, Routes.route_ids(session)[route_name]), route_name)


def model_frequency(train_list, route_name):
    c = Counter([convert_to_model(x) for x in train_list])
    if route_name == RED_LINE:
        c['1500-1700'] = c['1500'] + c['1600'] + c['1500']
        del c['1500'], c['1600'], c['1700']
    return {
        'counts': [x[0] for x in c.most_common()],
        'labels': [x[1] for x in c.most_common()]
    }


def convert_to_model(lead):
    """
    Converts 01876 or 1876 to 1800
    """
    return lead[-4:][0:2] + '00'


def prune_lead_list(list):
    """
    :param list: A list of lead cars
    :return: A list of lead cars without Nones or non-numerics
    """
    return [x for x in list if x and x.isdigit()]





