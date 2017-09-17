"""
Tests for zippy.parser
"""

import pytest
from zippy import inserter, parser, connector
from zippy.models import Province, Municipality, City, ZipCode, ZipCodeRange
from mock import MagicMock, patch, ANY


@pytest.fixture
def session(engine):
    connector.setup(engine)
    with connector.session_scope() as session:
        yield session


@pytest.fixture
def headers(small_data):
    return parser.parse_headers(small_data)


def test_create_range(session):
    range = ZipCodeRange(id='123', min_num=10)
    session.add(range)
    session.commit()

    retrieved = session.query(ZipCodeRange).filter(ZipCodeRange.id == range.id).first()
    assert retrieved == range


def test_create_zipcode(session):
    code = ZipCode(code='1234XY')
    range = ZipCodeRange(id='156', min_num=10, max_num=100)
    code.ranges.append(range)
    session.add(code)
    session.commit()

    retrieved = session.query(ZipCodeRange).filter(ZipCodeRange.id == range.id).first()
    assert retrieved == range

    code.ranges.append(ZipCodeRange(id='456', num_type='postcode'))
    session.commit()

    retrieved = session.query(ZipCode).filter(ZipCode.code == code.code).first()
    assert len(retrieved.ranges) == 2
    assert retrieved.ranges[1].num_type == 'postcode'


def test_append(session):
    province = Province(code='T')
    muni = Municipality(municipality_id='test_municipality', provinces=[province])
    city = City(id=12, municipalities=[muni])
    code = ZipCode(code='1234XY', cities=[city])
    range = ZipCodeRange(id='123', zipcode=code)

    session.add(range)
    session.commit()

    other_code, created = inserter.get_or_create(session, ZipCode, code='1234XY')
    assert not created
    other_range = ZipCodeRange(id='456', zipcode=other_code)
    session.add(other_range)
    session.commit()

    retrieved = session.query(ZipCode).filter(ZipCode.code == code.code).first()
    assert len(retrieved.ranges) == 2


def test_insert(small_data, session, headers):
    for line_num, vals in parser.parse_data(small_data, headers, 2):
        inserter.insert(session, vals)

    retrieved_city = session.query(City).filter(City.city_id == '1082').first()
    assert len(retrieved_city.zipcodes) == 10
