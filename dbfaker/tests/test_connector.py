"""
Tests dbfaker.connector
"""

import pytest
from dbfaker import connector


def test_setup():
    engine = connector.connect('postgres', 'root', 'zippy_tester')
    base = connector.setup(engine)

    assert base.classes
    assert base.classes.city