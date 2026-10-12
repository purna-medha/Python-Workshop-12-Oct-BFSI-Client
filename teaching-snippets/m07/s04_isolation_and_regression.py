# Tests need known starting conditions independent of execution order. Fixtures
# provide fresh setup. A discovered bug becomes a regression test by describing
# the observable promise it violated, without depending on private mechanics.
#
# Use conftest.py's fresh cart and preserve checkout-time facts across later changes.

from m03.cart import ShoppingCart


def test_carts_are_independent(cart):
    other_cart = ShoppingCart()
    cart.add("1", 2)
    assert cart.quantities == {"1": 2}
    assert other_cart.quantities == {}


def test_checkout_preserves_snapshot_and_clears_cart(cart):
    cart.add("1", 2)
    order = cart.checkout()
    assert cart.quantities == {}
    cart.add("1", 5)
    assert order.lines[0].quantity == 2
    assert order.total_paise == 99800
    assert cart.quantities == {"1": 5}


# Run: uv run --extra dev pytest m07/s04_isolation_and_regression.py -q
# If checkout retained live cart references, these snapshot assertions would expose it.
