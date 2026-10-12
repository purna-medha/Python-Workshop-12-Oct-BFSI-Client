# M7 companion: pytest discovers this fixture for tests in this directory.
import pytest
from m03.cart import ShoppingCart


@pytest.fixture
def cart():
    return ShoppingCart()           # Default function scope: fresh per test.
