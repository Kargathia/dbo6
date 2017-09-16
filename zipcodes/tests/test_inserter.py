"""
Tests for zippy.parser
"""

import pytest
from zippy import inserter
from zippy.models import Province, Municipality, City, ZipCode, ZipCodeRange
from mock import MagicMock, patch, ANY


@pytest.fixture
def engine():
    engine = inserter.connect('postgres', 'root', 'zippy_tester')
    inserter.recreate_database(engine)
    return engine


@pytest.fixture
def session(engine):
    return inserter.setup(engine)


def test_mock_connect(mocker):
    alch_mock = mocker.patch('zippy.inserter.sqlalchemy')
    inserter.connect('user', 'pw', 'all_your_databases')

    alch_mock.create_engine.assert_called_once_with(
        'postgresql://user:pw@localhost:5432/all_your_databases',
        client_encoding='utf8')


def test_create_range(session):
    s = session()
    s.add(ZipCodeRange())
