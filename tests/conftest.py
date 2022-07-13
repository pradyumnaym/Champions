import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Champions, Base
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="function")
def engine():
    """ Create Engine """
    return create_engine(f"{os.environ.get('DB_CONNECTION_STRING')}")


@pytest.fixture(scope="function")
def tables(engine):
    """ Create tables """
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(tables, engine):
    """ Create session """
    Session = sessionmaker(bind=engine)
    yield Session()
    

@pytest.fixture
def populate_db(tables,db_session):
    """ Populate database """
    Session = db_session
    champion1 = Champions(name="Kalika", 
                        biography="Mental health expert in career counselling", 
                        linkedin="linkedin.com/in/kalika-1345",
                        msr_profile="msr.com/kalika-2345",
                        avatar="profile_kalika.png",
                        order=1)
    with Session as session:
        session.add(champion1)
        session.commit()





