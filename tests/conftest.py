import os

import pytest
from fastapi.testclient import TestClient


# Before importing oblique, set some options specifically for testing
# Importing oblique will load the configuration, so this should be done before !
os.environ["OBLIQUE_DB"] = "memory"


import oblique  # noqa: E402
from oblique.database import SessionLocal, crud  # noqa: E402


@pytest.fixture(scope="module")
def db():
    # Create the tables for the in-memory DB
    crud.create_tables()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db):
    # Use DB fixture to ensure the tables were created

    yield TestClient(oblique.serve.get_main_app())
