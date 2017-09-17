"""
Responsible for inserting raw value dicts into the DB as well-formed objects
"""

import logging
import sqlalchemy
from sqlalchemy.orm import noload
from sqlalchemy.sql.expression import ClauseElement
from zippy import models
from zippy.models import Province, Municipality, City, ZipCode, ZipCodeRange


def get_or_create(session, model, avoid=None, **kwargs):
    qr = session.query(model).filter_by(**kwargs)
    if avoid:
        qr = qr.options(noload(*avoid))

    instance = qr.first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
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
    return get_or_create(session, ZipCode, avoid=['ranges'],
                         code=vals['POSTCODE'])


def add_city(session, vals):
    return get_or_create(session, City, avoid=['zipcodes'],
                         city_id=vals['CITY_ID'],
                         name=vals['CITY'])


def add_municipality(session, vals):
    return get_or_create(session, Municipality, avoid=['cities'],
                         municipality_id=vals['MUNICIPALITY_ID'],
                         name=vals['MUNICIPALITY'])


def add_province(session, vals):
    return get_or_create(session, Province, avoid=['municipalities'],
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
