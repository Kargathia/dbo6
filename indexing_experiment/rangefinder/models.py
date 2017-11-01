"""
Database models for zippy
"""

from sqlalchemy import Table, Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


province_municipality = Table(
    'province_municipality',
    Base.metadata,
    Column('fk_province', String, ForeignKey('province.code')),
    Column('fk_municipality', Integer, ForeignKey('municipality.id'))
)

municipality_city = Table(
    'municipality_city',
    Base.metadata,
    Column('fk_municipality', Integer, ForeignKey('municipality.id')),
    Column('fk_city', Integer, ForeignKey('city.id')),
)


city_zipcode = Table(
    'city_zipcode',
    Base.metadata,
    Column('fk_city', Integer, ForeignKey('city.id')),
    Column('fk_zipcode', String, ForeignKey('zipcode.code'))
)


class Province(Base):
    __tablename__ = 'province'

    code = Column(String, primary_key=True)
    name = Column(String)

    municipalities = relationship('Municipality',
                                  secondary=province_municipality,
                                  backref='provinces')


class Municipality(Base):
    __tablename__ = 'municipality'

    id = Column(Integer, primary_key=True)
    municipality_id = Column(String)
    name = Column(String)

    cities = relationship('City',
                          secondary=municipality_city,
                          backref='municipalities')


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    city_id = Column(String)
    name = Column(String)

    zipcodes = relationship('ZipCode',
                            secondary=city_zipcode,
                            backref='cities')


class ZipCode(Base):
    __tablename__ = 'zipcode'

    code = Column(String, primary_key=True)
    ranges = relationship('ZipCodeRange',
                          back_populates='zipcode')


class ZipCodeRange(Base):
    __tablename__ = 'zipcoderange'

    id = Column(String, primary_key=True)
    zipcode_code = Column(String, ForeignKey('zipcode.code'))
    zipcode = relationship('ZipCode', back_populates='ranges')

    street = Column(String)
    min_num = Column(Integer)
    max_num = Column(Integer)
    num_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rd_x = Column(Float)
    rd_y = Column(Float)
    last_change = Column(String)
