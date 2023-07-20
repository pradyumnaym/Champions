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


def update_champion(
    champion_id, name, biography, linkedin, msr_profile, avatar, order, new_field, session: Session
):
    """Return updated champion data"""
    if champion_id is not None:
        query = select(ChampionsModel).filter(ChampionsModel.id == champion_id)
        with session as session:
            champion = session.execute(query).scalars().unique().one()
            if name is not None:
                champion.name = name
            if biography is not None:
                champion.biography = biography
            if linkedin is not None:
                champion.linkedin = linkedin
            if msr_profile is not None:
                champion.msr_profile = msr_profile
            if avatar is not None:
                champion.avatar = avatar
            if order is not None:
                champion.order = order
            if new_field is not None:
                champion.new_field = new_field
            session.commit()
        return champion
    schema = ChampionsModel(
        name=name,
        biography=biography,
        linkedin=linkedin,
        msr_profile=msr_profile,
        avatar=avatar,
        order=order,
        new_field=new_field,
    )
    with session as session:
        session.add(schema)
        session.commit()
    return schema
