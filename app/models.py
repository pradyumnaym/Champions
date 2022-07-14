from sqlalchemy import Integer, SmallInteger, String
from sqlalchemy.sql.schema import Column

from .database_config import Base


class Champions(Base):
    """Topics database model"""

    __tablename__ = "champions_table"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # name -> MHC Full name
    name = Column(String, nullable=True)

    # biography -> small description about themselfs
    biography = Column(String, nullable=True)

    # linkedin list -> link
    linkedin = Column(String, nullable=True)

    # MSR profile -> link
    msr_profile = Column(String, nullable=True)

    # avatar -> MHC photos
    avatar = Column(String, nullable=True)

    # order in which to display
    order = Column(SmallInteger, nullable=True)
