import pytest
from unittest import mock
import mongomock
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float, Date
from service.api.api import SportsBettingService

class Helpers:
    @staticmethod
    def sport_bet_api(storage):
        client = SportsBettingService(storage)
        return client
    

@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture
def db_name(request):
    service = request.config.getoption('--service')
    return service

@pytest.fixture
@mock.patch('storage.mysql.mysql.MySQLStorage')
def storage(mock_mysql, db_name):
    print(db_name)
    if db_name == 'mysql':
        return mock_mysql
    
def pytest_addoption(parser):
    parser.addoption(
        "--service", action="store", default="mysql"
    )

@pytest.fixture()
def mongo_mock():
    client = mongomock.MongoClient()
    return client

@pytest.fixture(scope='function')
def db():
    """Session for SQLAlchemy."""
    Base = declarative_base()  
    meta = Base.metadata
    engine = create_engine('sqlite://')
    Table('bettingmodel', meta, Column('id', Integer, primary_key=True, index=True), Column('league', String(20), index=True, nullable=False), Column('home_team', String(20), index=True), Column('away_team', String(20), index=True), Column('home_team_win_odds', Float(20), index=True), Column('away_team_win_odds', Float(20), index=True),  Column('draw_odds', Float(20), index=True), Column('game_date', Date(), index=True))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


    



