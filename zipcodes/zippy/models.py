"""
Database models for zippy
Component Province
Component Municipality
Component City
Component ZipCode
Component Range
"""


class Province:
    name = None
    code = None
    municipalities = None


class Municipality:
    name = None
    cities = None


class City:
    name = None
    zip_codes = None


class ZipCode:
    letters = None
    number = None
    ranges = None


class Range:
    min_num = None
    max_num = None
    num_type = None
    latitude = None
    longitude = None
    rd_x = None
    rd_y = None
