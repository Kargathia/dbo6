"""
Responsible for inserting raw value dicts into the DB as well-formed objects
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from zippy import models


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    engine = sqlalchemy.create_engine(url, client_encoding='utf8')

    # # We then bind the connection to MetaData()
    # meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return engine


def recreate_database(engine):
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)


def setup(engine):
    maker = sessionmaker()
    maker.configure(bind=engine)
    models.Base.metadata.create_all(engine)
    return maker


def insert(vals, session):
    pass