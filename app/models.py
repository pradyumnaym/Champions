from sqlalchemy import Integer, SmallInteger, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Column

from .db_conf import SQLALCHEMY_DATABASE_URL, Base


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

    # avatar -> MHC photos
    avatar = Column(String, nullable=True)

    # order in which to display
    order = Column(SmallInteger, nullable=True)


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)


# get database session
def get_db():
    """Yeilds database connection"""
    try:
        _db = SessionLocal()
        yield _db
    finally:
        _db.close()
