import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_CONNECTION_STRING

SQLALCHEMY_DATABASE_URL = f"{DB_CONNECTION_STRING}"

metadata = sqlalchemy.MetaData()
Base = declarative_base()
