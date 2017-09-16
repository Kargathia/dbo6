"""
Database models for zippy
"""

from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Province(Base):
    __tablename__ = 'province'
    code = Column(Integer, primary_key=True)
    name = Column(String)
    municipalities = relationship('Municipality',
                                  secondary='province_municipality',
                                  order_by='Municipality.name')


class Province


class Municipality(Base):
    __tablename__ = 'municipality'
    name = Column(String, primary_key=True)
    cities = relationship('City',
                          secondary='municipality_city',
                          order_by='City.name')


class City(Base):
    __tablename__ = 'city'
    name = Column(String, primary_key=True)
    cities = relationship('ZipCode',
                          secondary='city_zipcode',
                          order_by='ZipCode.id')


class ZipCode(Base):
    __tablename__ = 'zipcode'
    id = Column(Integer, primary_key=True)
    letters = Column(String)
    number = Column(Integer)
    last_change = Column(DateTime)
    ranges = relationship('ZipCodeRange',
                          order_by='ZipCodeRange.id')


class ZipCodeRange(Base):
    __tablename__ = 'zipcoderange'
    id = Column(Integer, primary_key=True)
    min_num = Column(Integer)
    max_num = Column(Integer)
    num_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rd_x = Column(Float)
    rd_y = Column(Float)
