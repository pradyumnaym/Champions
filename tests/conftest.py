import os

from app.models import Base, Champions
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


@pytest.fixture
def engine():
    """Create Engine"""
    return create_engine(f"{os.environ['DB_CONNECTION_STRING']}")


@pytest.fixture
def tables(engine):
    """Create tables"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(tables, engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session_local = session()
    yield session_local

    session_local.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def populate_db(tables, db_session):
    """Populate database"""
    session = db_session
    champion1 = Champions(
        name="Kalika",
        biography="Volunteer for mental health well being f employees",
        linkedin="linkedin.com/in/kalika-1345",
        msr_profile="msr.com/kalika-2345",
        avatar="profile_kalika.png",
        order=1,
    )
    with session as session:
        session.add(champion1)
        session.commit()
