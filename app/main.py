import os
import time

from app import models
from ariadne import MutationType, QueryType, gql, load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.contrib.federation.schema import make_federated_schema
from fastapi import FastAPI, Request

from .database_definitions import get_champion_by_id, get_mental_health_champions, update_champion
from .db import SessionLocal, engine
from .utils import get_logger, get_sas_url

APPLICATION_INSIGHTS_CONNECTION_STRING = os.environ["APPLICATION_INSIGHTS_CONNECTION_STRING"]
logger = get_logger(APPLICATION_INSIGHTS_CONNECTION_STRING=APPLICATION_INSIGHTS_CONNECTION_STRING)
properties = {"custom_dimensions": {"service": "champions"}}

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("./app/gql/")
type_defs = gql(type_defs)

# Create type instance for Query type defined in our schema...
query = QueryType()
mutation = MutationType()
champions = FederatedObjectType("Champions")

# ------------ QUERIES START HERE ------------------#


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    idem = request.headers["requestId"] if "requestId" in request.headers else None
    logger.info(f"rid={idem} start request path={request.url.path}", extra=properties)
    start_time = time.time()
    # request.scope["x-request-id"] = idem
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} path={request.url.path} completed_in={formatted_process_time} ms status_code={response.status_code} ",
        extra=properties,
    )

    return response


@champions.reference_resolver
def resolve_champions_data(_, info, representation):
    session = info.context["session"]
    return get_mental_health_champions(session)


@champions.field("avatar")
def resolve_image(obj, *_):
    print(obj)
    print(obj.avatar)
    if obj.avatar:
        return get_sas_url(url=obj.avatar)


@query.field("getMentalHealthChampions")
def resolve_get_champions_data(_, info):
    """Return sqlalchemy object for schema provided"""
    logger.info("Query: getMentalHealthChampions ran successfully")
    session = info.context["session"]
    return get_mental_health_champions(session)


@query.field("champions")
def resolve_champions(_, info):
    """Return all the champions from database"""
    logger.info("Query: champions ran successfully")
    session = info.context["session"]
    return get_mental_health_champions(session=session)


@query.field("champion")
def resolve_champion(_, info, id):
    """Return champion data by id"""
    logger.info("Query: champion ran successfully")
    session = info.context["session"]
    return get_champion_by_id(id=id, session=session)


@mutation.field("champion")
def resolve_update_champion(
    _, info, champion_id, name, biography, linkedin, msr_profile, avatar, order
):
    """Create/Update champion"""
    logger.info("Mutation: champion ran successfully")
    session = info.context["session"]
    result = update_champion(
        champion_id=champion_id,
        name=name,
        biography=biography,
        linkedin=linkedin,
        msr_profile=msr_profile,
        avatar=avatar,
        order=order,
        session=session,
    )
    return result


def get_context_value(request):
    return {"request": request, "session": SessionLocal()}


# -------- QUERIES END HERE ------------#


schema = make_federated_schema(type_defs, [query, mutation, champions])  # type: ignore
app.mount("/", GraphQL(schema, context_value=get_context_value))
