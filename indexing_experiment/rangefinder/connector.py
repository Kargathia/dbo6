"""
Responsible for connecting to the database, and creating the session object
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from contextlib import contextmanager
from rangefinder import models


Session = sessionmaker()


def connect(user, password, db, host='localhost', port=5432):
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    return sqlalchemy.create_engine(url, client_encoding='utf8')


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
