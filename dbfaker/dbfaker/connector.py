"""
Responsible for connecting to the database, and creating the session object
"""

import sqlalchemy
from contextlib import contextmanager
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


def connect(user, password, db, host='localhost', port=5432):
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    return sqlalchemy.create_engine(url, client_encoding='utf8')


def setup(engine):
    # reflect the tables
    base = automap_base()
    base.prepare(engine, reflect=True)
    return base


def startup(user, password, db, host='localhost', port=5432):
    engine = connect(user, password, db, host, port)
    base = setup(engine)
    return engine, base

@contextmanager
def session_scope(engine):
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
