'''
Fixtures for pytest should be added here
'''

import pytest
import os
from mock import mock_open
from zippy import parser


def test_parse_headers(small_data):
    assert parser.parse_headers(small_data) == [
        'ID', 'POSTCODE', 'POSTCODE_ID', 'PNUM',
        'PCHAR', 'MINNUMBER', 'MAXNUMBER', 'NUMBERTYPE',
        'STREET', 'CITY', 'CITY_ID', 'MUNICIPALITY',
        'MUNICIPALITY_ID', 'PROVINCE', 'PROVINCE_CODE',
        'LAT', 'LON', 'RD_X', 'RD_Y', 'LOCATION_DETAIL', 'CHANGED_DATE'
    ]


def test_parse_partial(small_data):
    headers = parser.parse_headers(small_data)
    parsed = {line: vals for line, vals in
              parser.parse_data(small_data, headers, 2, 5)}
    assert not parsed.get(1)
    assert parsed[2]['MINNUMBER'] == '4'
    assert parsed[3]['PCHAR'] == 'AA'
    assert parsed[5]['RD_Y'] == '523633.730181818'
    assert not parsed.get(6)


def test_parse_all(small_data):
    headers = parser.parse_headers(small_data)
    parsed = {line: vals for line, vals in
              parser.parse_data(small_data, headers, 2)}
    assert parsed[11]['CHANGED_DATE'] == '2014-04-10 13:20:28'
