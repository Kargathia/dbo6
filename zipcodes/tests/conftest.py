"""
Declares global fixtures
"""

import pytest
import os
from zippy import connector


@pytest.fixture
def small_data():
    return os.path.abspath('tests/testdata/testdata.csv')


@pytest.fixture
def engine():
    engine = connector.connect('postgres', 'root', 'zippy_tester')
    connector.recreate_database(engine)
    return engine
