from app import models
from ariadne import QueryType, gql, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from .database_definitions import get_mental_health_champions
from .db import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("./app/gql/")
type_defs = gql(type_defs)

# Create type instance for Query type defined in our schema...
query = QueryType()


@query.field("getMentalHealthChampions")
def resolve_get_welcome_screens(_, info):
    """Return sqlalchemy object for schema provided"""
    session = info.context["session"]
    return get_mental_health_champions(session)


schema = make_executable_schema(type_defs, query)  # type: ignore
app.mount("/", GraphQL(schema, context_value={"session": SessionLocal()}))
