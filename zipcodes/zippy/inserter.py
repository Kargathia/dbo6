"""
Responsible for inserting raw value dicts into the DB as well-formed objects
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy_utils import database_exists, create_database, drop_database
from contextlib import contextmanager
from zippy import models
from zippy.models import Province, Municipality, City, ZipCode, ZipCodeRange

Session = sessionmaker()


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    return sqlalchemy.create_engine(url, client_encoding='utf8')


def recreate_database(engine):
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)


def setup(engine):
    Session.configure(bind=engine)
    models.Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def add_zipcode_range(session, vals):
    range = ZipCodeRange(id=vals['ID'],
                         street=vals['STREET'],
                         min_num=int(vals['MINNUMBER']),
                         max_num=int(vals['MAXNUMBER']),
                         num_type=vals['NUMBERTYPE'],
                         latitude=float(vals['LAT']),
                         longitude=float(vals['LON']),
                         rd_x=float(vals['RD_X']),
                         rd_y=float(vals['RD_Y']),
                         last_change=vals['CHANGED_DATE']
                         )
    session.add(range)
    return range, True


def add_zipcode(session, vals):
    return get_or_create(session, ZipCode,
                         code=vals['POSTCODE'])


def add_city(session, vals):
    return get_or_create(session, City,
                         city_id=vals['CITY_ID'],
                         name=vals['CITY'])


def add_municipality(session, vals):
    return get_or_create(session, Municipality,
                         municipality_id=vals['MUNICIPALITY_ID'],
                         name=vals['MUNICIPALITY'])


def add_province(session, vals):
    return get_or_create(session, Province,
                         code=vals['PROVINCE_CODE'],
                         name=vals['PROVINCE'])


def insert(session, vals):
    range, range_created = add_zipcode_range(session, vals)
    zipcode, zipcode_created = add_zipcode(session, vals)
    zipcode.ranges.append(range)

    if not zipcode_created:
        return

    city, city_created = add_city(session, vals)
    city.zipcodes.append(zipcode)

    if not city_created:
        return

    municipality, muni_created = add_municipality(session, vals)
    municipality.cities.append(city)

    if not muni_created:
        return

    province, province_created = add_province(session, vals)
    province.municipalities.append(municipality)
