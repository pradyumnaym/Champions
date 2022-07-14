from app.database_definitions import get_mental_health_champions


def test_get_mental_health_champions(db_session, populate_db):
    """Testing get champions"""
    session = db_session
    champions = get_mental_health_champions(session)
    assert len(champions) == 1
