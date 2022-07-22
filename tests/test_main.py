from app.database_definitions import get_mental_health_champions
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main() -> None:
    """Testing root path"""
    response = client.get("/")
    assert response.status_code == 200


def test_get_mental_health_champions(db_session, populate_db):
    """Testing get champions"""
    session = db_session
    champions = get_mental_health_champions(session)
    assert len(champions) == 1
