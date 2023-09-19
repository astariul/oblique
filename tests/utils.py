import os

import pytest
from fastapi.testclient import TestClient


# Before importing oblique, set some options specifically for testing
# Importing oblique will load the configuration, so this should be done before !
os.environ["OBLIQUE_DB"] = "memory"


import oblique  # noqa: E402


@pytest.fixture
def client():
    # Create the tables for the in-memory DB
    oblique.database.crud.create_tables()

    yield TestClient(oblique.serve.get_main_app())
