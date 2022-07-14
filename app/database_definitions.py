from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Champions as ChampionsModel


def get_mental_health_champions(session: Session):
    """Return's mental health champions sql objects"""
    query = select(ChampionsModel)

    with session as session:
        result = session.execute(query).scalars().unique().all()

    return result
