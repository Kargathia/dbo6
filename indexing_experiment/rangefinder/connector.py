"""
Responsible for connecting to the database, and creating the session object
"""

import time
import logging
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from contextlib import contextmanager
from rangefinder import models


Session = sessionmaker()


@event.listens_for(Engine, 'before_cursor_execute')
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    context._query_start_time = time.time()
    logging.debug('Start Query:\n%s' % statement)
    # Modification for StackOverflow answer:
    # Show parameters, which might be too verbose, depending on usage..
    logging.debug('Parameters:\n%r' % (parameters,))


@event.listens_for(Engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - context._query_start_time
    logging.debug('Query Complete!')

    # Modification for StackOverflow: times in milliseconds
    logging.debug('Total Time: %.02fms' % (total * 1000))


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
