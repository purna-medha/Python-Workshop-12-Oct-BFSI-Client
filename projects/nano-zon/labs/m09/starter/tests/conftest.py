# Fresh state keeps tests independent; later fixtures supply a real temporary database.
import pytest
from nanozon.cart import ShoppingCart
from nanozon.catalog import seed_products


@pytest.fixture
def products():
    return seed_products()


@pytest.fixture
def cart(products):
    return ShoppingCart(products)


@pytest.fixture
def store(tmp_path):
    from nanozon.storage import SQLiteStore
    return SQLiteStore(tmp_path / "shop.sqlite")


@pytest.fixture
def client(store):
    from fastapi.testclient import TestClient
    from nanozon.api import create_app
    with TestClient(create_app(store)) as client:
        yield client
