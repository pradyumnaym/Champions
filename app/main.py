from app import models
from ariadne import QueryType, gql, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.contrib.federation.schema import make_federated_schema
from fastapi import FastAPI

from .database_definitions import get_mental_health_champions
from .db import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("./app/gql/")
type_defs = gql(type_defs)

# Create type instance for Query type defined in our schema...
query = QueryType()
champions = FederatedObjectType("Champions")

# ------------ QUERIES START HERE ------------------#

@champions.reference_resolver
def resolve_champions_data(_, info, representation):
    session = info.context["session"]
    return get_mental_health_champions(session)

@query.field("getMentalHealthChampions")
def resolve_get_welcome_screens(_, info):
    """Return sqlalchemy object for schema provided"""
    session = info.context["session"]
    return get_mental_health_champions(session)


def get_context_value(request):
    return {"request": request, "session": SessionLocal()}


# -------- QUERIES END HERE ------------#


schema = make_federated_schema(type_defs, [query])  # type: ignore
app.mount("/", GraphQL(schema, context_value=get_context_value))
