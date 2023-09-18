"""Dependencies used in both the web-app and the API."""
from oblique.database import SessionLocal


def get_db() -> SessionLocal:
    """FastAPI dependency to create a DB Session.

    Yields:
        SessionLocal: DB Session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
