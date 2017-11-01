"""
Adds and removes indexes to previously defined columns
"""

from sqlalchemy import Index, func
from rangefinder.models import ZipCodeRange


def add_extension(session):
    session.execute('CREATE EXTENSION IF NOT EXISTS earthdistance CASCADE')


def drop_index(session, index_name='rangefinder'):
    session.execute('DROP INDEX IF EXISTS {}'.format(index_name))


def add_index(engine, index_type, index_name='rangefinder'):
    op_func = func.ll_to_earth(ZipCodeRange.latitude, ZipCodeRange.longitude)
    index = Index(index_name, op_func, postgresql_using=index_type)
    index.create(bind=engine)
