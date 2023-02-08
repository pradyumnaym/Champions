from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Champions as ChampionsModel


def get_mental_health_champions(session: Session):
    """Return's mental health champions sql objects"""
    query = select(ChampionsModel)

    with session as session:
        result = session.execute(query).scalars().unique().all()

    return result


def get_champion_by_id(id: int, session: Session):
    """Return champion data for given id"""
    query = select(ChampionsModel).filter(ChampionsModel.id == id)
    with session as session:
        result = session.execute(query).scalars().unique().one()
    return result


def update_champion(id, champion_data, session: Session):
    """Return updated champion data"""
    query = select(ChampionsModel).filter(ChampionsModel.id == id)
    with session as session:
        champion = session.execute(query).scalars().unique().one()
        if champion_data["name"]:
            champion.name = champion_data["name"]
        if champion_data["biography"]:
            champion.biography = champion_data["biography"]
        if champion_data["linkedin"]:
            champion.linkedin = champion_data["linkedin"]
        if champion_data["msr_profile"]:
            champion.msr_profile = champion_data["msr_profile"]
        if champion_data["avatar"]:
            champion.avatar = champion_data["avatar"]
        if champion_data["order"]:
            champion.order = champion_data["order"]


def create_champion(champion_data, session: Session):
    """Create a champion profile"""
    schema = ChampionsModel(
        name=champion_data["name"],
        biography=champion_data["biography"],
        linkedin=champion_data["linkedin"],
        msr_profile=champion_data["msr_profile"],
        avatar=champion_data["avatar"],
        order=champion_data["order"],
    )
