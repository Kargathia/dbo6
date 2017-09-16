"""
Declares global fixtures
"""

import pytest
import os


@pytest.fixture
def small_data():
    return os.path.abspath('tests/testdata/testdata.csv')
