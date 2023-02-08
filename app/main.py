from app import models
from ariadne import MutationType, QueryType, gql, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.contrib.federation.schema import make_federated_schema
from fastapi import FastAPI

from .database_definitions import (
    create_champion,
    get_champion_by_id,
    get_mental_health_champions,
    update_champion,
)
from .db import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("./app/gql/")
type_defs = gql(type_defs)

# Create type instance for Query type defined in our schema...
query = QueryType()
mutation = MutationType()
champions = FederatedObjectType("Champions")

# ------------ QUERIES START HERE ------------------#


@champions.reference_resolver
def resolve_champions_data(_, info, representation):
    session = info.context["session"]
    return get_mental_health_champions(session)


@query.field("getMentalHealthChampions")
def resolve_get_champions_data(_, info):
    """Return sqlalchemy object for schema provided"""
    session = info.context["session"]
    return get_mental_health_champions(session)


@query.field("champions")
def resolve_champions(_, info):
    """Return all the champions from database"""
    session = info.context["session"]
    return get_mental_health_champions(session=session)


@query.field("champion")
def resolve_champion(_, info, id):
    """Return champion data by id"""
    session = info.context["session"]
    return get_champion_by_id(id=id, session=session)


@mutation.field("addChampion")
def resolve_add_champion(_, info, champion_data):
    """Create a ne champion from champion data"""
    session = info.context["session"]
    return create_champion(champion_data=champion_data, session=session)


@mutation.field("updateChampion")
def resolve_update_champion(_, info, id, champion_data):
    """Create a ne champion from champion data"""
    session = info.context["session"]
    return update_champion(id=id, champion_data=champion_data, session=session)


def get_context_value(request):
    return {"request": request, "session": SessionLocal()}


# -------- QUERIES END HERE ------------#


schema = make_federated_schema(type_defs, [query, mutation])  # type: ignore
app.mount("/", GraphQL(schema, context_value=get_context_value))
