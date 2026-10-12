# M8 companion: fresh real storage, with the API's connection boundary overridden.
import pytest
from fastapi.testclient import TestClient
from m06.api import create_app
from m06.api_dependencies import get_connection
from m06.database import connect, initialize


@pytest.fixture
def database_path(tmp_path):
    path = tmp_path / "test-shop.sqlite"
    with connect(path) as connection:
        initialize(connection)
    return path


@pytest.fixture
def client(database_path):
    # The default path is never opened: every storage route uses the override.
    app = create_app("unused.sqlite")

    def isolated_connection():
        # Create the connection in the request's thread, not the fixture's thread.
        with connect(database_path) as connection:
            yield connection

    app.dependency_overrides[get_connection] = isolated_connection
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()
