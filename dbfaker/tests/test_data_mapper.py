"""
Tests dbfaker.data_mapper
"""

import pytest
from dbfaker import connector, data_mapper


@pytest.fixture
def conn_args():
    return ['postgres', 'root', 'zippy']


def test_map_column(conn_args):
    engine, base = connector.startup(*conn_args)

    k, v = data_mapper.map_column(base.classes.zipcoderange.longitude)
    assert k == 'longitude'
    assert v


def test_map_table(conn_args):
    engine, base = connector.startup(*conn_args)

    k, v = data_mapper.map_table(base.classes.zipcoderange)
    assert k == 'zipcoderange'
    assert v['longitude']


def test_map_base(conn_args):
    engine, base = connector.startup(*conn_args)

    mapped = data_mapper.map_base(base)
    assert len(mapped) == 5
    assert mapped['zipcoderange']['longitude']
