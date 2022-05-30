import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(".env")

# postgres sql connection string
SQLALCHEMY_DATABASE_URL = f"{os.environ.get('DB_CONNECTION_STRING')}"
metadata = sqlalchemy.MetaData()
Base = declarative_base()
