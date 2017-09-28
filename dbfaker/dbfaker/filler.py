"""
Reads the database spec, and generates random data based on it
"""

import sys
import requests
from dbfaker import connector
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import inspect
import uuid
from pprint import pprint


def create(session, model, kwargs):
    params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
    instance = model(**params)
    session.add(instance)
    return instance


def request_value(faker_type):
    return requests.post('http://localhost:8081/fake', json={'type': faker_type}).text


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

        pytype = spec['pytype']
        if pytype:
            val = __builtins__[pytype](val)

        yield name, val
