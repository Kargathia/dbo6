"""
Reads the database spec, and generates random data based on it
"""

import requests
from dbfaker import connector
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import inspect
import uuid


def create(session, model, kwargs):
    params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
    instance = model(**params)
    session.add(instance)
    return instance


def request_value(faker_type):
    return {
        'faker.random.number': lambda: 12.3,
        'faker.random.arrayIndex': lambda: 9,
        'faker.random.word': lambda: 'testey',
        'faker.random.word.unique': lambda: str(uuid.uuid4())
    }[faker_type]()
    # query API for values


def fill_database(engine, base, spec):
    for k, v in spec.items():
        with connector.session_scope(engine) as session:
            fill_table(session, base, k, v)


def fill_table(session, base, table_name, table_spec):
    model = getattr(base.classes, table_name)
    count = table_spec['num_generated']
    columns = table_spec['columns']

    for i in range(count):
        create(session, model, {k: v for k, v in get_column_val(columns)})


def get_column_val(columns):
    for name, spec in columns.items():
        filler = spec['filler']
        val = None
        if not filler:
            pass
        elif isinstance(filler, dict):
            pass
        else:
            val = request_value(filler)

        yield name, val
