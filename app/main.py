from ariadne import (QueryType, gql, load_schema_from_path,
                     make_executable_schema)
from ariadne.asgi import GraphQL

from .db_definitions import get_mental_health_champions
from .models import get_db

type_defs = load_schema_from_path("./app/gql/")
type_defs = gql(type_defs)

# Create type instance for Query type defined in our schema...
query = QueryType()


@query.field("getMentalHealthChampions")
def resolve_get_welcome_screens(_, info):
    """Return sqlalchemy object for schema provided"""
    return get_mental_health_champions()


get_db()
schema = make_executable_schema(type_defs, query)  # type: ignore
app = GraphQL(schema)
