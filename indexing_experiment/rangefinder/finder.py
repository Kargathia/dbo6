"""
Performs various lookup functions in the zipcode database
"""


import logging
from sqlalchemy import func
from rangefinder.models import ZipCodeRange


def find_closest(session, lat, long, limit):
    # Calculating each zipcode range's distance from Target
    loc_target = func.ll_to_earth(lat, long)
    loc_ziprange = func.ll_to_earth(ZipCodeRange.latitude, ZipCodeRange.longitude)
    distance_func = func.earth_distance(loc_target, loc_ziprange)

    query = session.query(ZipCodeRange, distance_func)\
        .order_by(distance_func)\
        .limit(limit)

    # Resultset is no longer list of Ranges, but a list of tuples.
    result = query.all()
    mapped = []
    for row in result:
        zipcoderange = row[0]
        zipcoderange.distance = row[1]
        mapped.append(zipcoderange)

    logging.info('closest range(zipcode= {}, lat={},long={}) with distance {}'.format(
        mapped[0].zipcode_code,
        mapped[0].latitude,
        mapped[0].longitude,
        mapped[0].distance))
    return mapped
