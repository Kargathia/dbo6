"""
Tests zippy.connector
"""

import pytest
from zippy import connector
from mock import MagicMock


def test_mock_connect(mocker):
    alch_mock = mocker.patch('zippy.connector.sqlalchemy')
    connector.connect('user', 'pw', 'all_your_databases')

    alch_mock.create_engine.assert_called_once_with(
        'postgresql://user:pw@localhost:5432/all_your_databases',
        client_encoding='utf8')


def test_recreate(mocker):
    exist_mock = mocker.patch('zippy.connector.database_exists')
    drop_mock = mocker.patch('zippy.connector.drop_database')
    create_mock = mocker.patch('zippy.connector.create_database')
    engine = MagicMock(url='url')

    connector.recreate_database(engine)

    exist_mock.assert_called_once_with('url')
    drop_mock.assert_called_once_with('url')
    create_mock.assert_called_once_with('url')


def test_session_scope(mocker):
    session_mock = mocker.patch.object(connector, 'Session').return_value

    with connector.session_scope() as session:
        assert session == session_mock
        assert session_mock.commit.call_count == 0
        assert session_mock.close.call_count == 0

    assert session_mock.commit.call_count == 1
    assert session_mock.rollback.call_count == 0
    assert session_mock.close.call_count == 1


def test_session_scope_raise(mocker):
    session_mock = mocker.patch.object(connector, 'Session').return_value

    with pytest.raises(EnvironmentError):
        with connector.session_scope() as session:
            raise EnvironmentError('boo!')

    assert session_mock.commit.call_count == 0
    assert session_mock.rollback.call_count == 1
    assert session_mock.close.call_count == 1
