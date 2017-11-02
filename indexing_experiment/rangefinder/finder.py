"""
Performs various lookup functions in the zipcode database
"""


import logging
from pprint import pformat
from sqlalchemy import func
from rangefinder.models import ZipCodeRange
from rangefinder.explainer import Explain


def find_closest(session, lat, long, limit):
    # Calculating each zipcode range's distance from Target
    radius = 100
    loc_target = func.ll_to_earth(lat, long)
    loc_ziprange = func.ll_to_earth(ZipCodeRange.latitude, ZipCodeRange.longitude)
    # distance_func = func.earth_box(func.ll_to_earth(loc_target, loc_ziprange), 100)

    query = session.query(ZipCodeRange).filter(
        func.earth_box(func.ll_to_earth(lat, long), radius
                       ).op('@>')(func.ll_to_earth(ZipCodeRange.latitude, ZipCodeRange.longitude))
    ).limit(limit)

    query_params = {'ll_to_earth_1': lat,
                    'll_to_earth_2': long,
                    'param_1': limit}

    analysis = session.execute(Explain(query, analyze=True), query_params).fetchall()
    logging.info(pformat(analysis))

    # Resultset is no longer list of Ranges, but a list of tuples.
    result = query.all()

    [logging.info('found zipcoderange(zipcode={}, lat={},long={})'.format(
        r.zipcode_code,
        r.latitude,
        r.longitude)) for r in result]
    return result
