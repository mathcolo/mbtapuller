from Classes import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Functions import *

def pytest_funcarg__session(request):
    db = create_engine('sqlite:///mbta.db', echo=False)
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    session = Session()
    return session

def pytest_funcarg__triprecord(request, session):
    record = session.query(TripRecord).first()
    return record

def pair_equal(pair1, pair2):
    if pair1 == pair2 or pair1 == pair2[::-1]:
        return True
    else:
        return False

def test_find_segment_ALEWIFE(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.397805, -71.131591)),
           ('Alewife', 'Davis'))

def test_find_segment_ALEWIFE2(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.397969, -71.135044)),
           ('Alewife', 'Davis'))

def test_find_segment_DAVIS(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.392056, -71.119060)),
           ('Davis', 'Porter'))

def test_find_segment_PORTER(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.383352, -71.119532)),
           ('Porter', 'Harvard'))

def test_find_segment_HARVARD(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.368863, -71.110090)),
           ('Harvard', 'Central'))

def test_find_segment_CENTRAL(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.363198, -71.096354)),
           ('Central', 'Kendall/MIT'))

def test_find_segment_MIT(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.361715, -71.078269)),
           ('Kendall/MIT', 'Charles/MGH'))

def test_find_segment_MGH(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.359134, -71.067219)),
           ('Charles/MGH', 'Park Street'))

def test_find_segment_PARK(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.355893, -71.061459)),
           ('Park Street', 'Downtown Crossing'))

def test_find_segment_DOWNTOWN(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.353835, -71.057797)),
           ('Downtown Crossing', 'South Station'))

def test_find_segment_SOUTH(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.347594, -71.053991)),
           ('South Station', 'Broadway'))

def test_find_segment_BROADWAY(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.336328, -71.056950)),
           ('Broadway', 'Andrew'))

def test_find_segment_ANDREW(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.327684, -71.057934)),
           ('Andrew', 'JFK/Umass'))

def test_find_segment_JFK(session, triprecord):
    assert pair_equal(find_segment(triprecord, session, (42.316547, -71.052152)),
           ('JFK/Umass', 'Savin Hill'))

def test_find_segment_BRAINTREEBRANCH(session, triprecord):
    triprecord.trip_id = 3
    assert pair_equal(find_segment(triprecord, session, (42.300707, -71.054977)),
           ('JFK/Umass', 'North Quincy'))
