# M7: assertions describe observable promises, not private implementation details.
import pytest
from nanozon.calculations import calculate_line_total
from nanozon.cart import ShoppingCart
from nanozon.catalog import select_products
from nanozon.memory import MemoryStore
from nanozon.orders import build_order


@pytest.mark.parametrize("price, quantity, expected", [
    (49900, 2, 99800), (89900, 3, 269700), (0, 1, 0),
])
def test_line_total(price, quantity, expected):
    actual = calculate_line_total(price, quantity)
    # ANSWER m07 exact_total BEGIN
    assert actual == expected
    # ANSWER m07 exact_total END


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_invalid_quantity(quantity):
    # ANSWER m07 rejected_quantity BEGIN
    with pytest.raises(ValueError, match="positive integer"):
        calculate_line_total(49900, quantity)
    # ANSWER m07 rejected_quantity END


def test_search_and_zero_bound(products):
    matches = select_products(products, query="CABLE")
    # ANSWER m07 search_boundaries BEGIN
    assert [product.product_id for product in matches] == ["1"]
    assert select_products(products, maximum_paise=0) == []
    assert select_products(products, query="does not exist") == []
    # ANSWER m07 search_boundaries END


def test_cart_operations_and_independence(cart):
    other_cart = ShoppingCart()
    cart.add("1", 2)
    cart.add("1")
    cart.update("1", 4)
    assert cart.subtotal_paise == 199600
    assert other_cart.items == {}
    cart.remove("1")
    assert cart.subtotal_paise == 0


def test_order_snapshot_and_checkout_reset(cart):
    cart.add("1", 2)
    order = cart.checkout(MemoryStore())
    cart.add("1", 5)
    # ANSWER m07 order_snapshot BEGIN
    assert order.lines[0].quantity == 2
    assert order.lines[0].unit_price_paise == 49900
    assert order.total_paise == 99800
    assert cart.items["1"].quantity == 5
    # ANSWER m07 order_snapshot END


def test_empty_and_unknown_checkout(products):
    with pytest.raises(ValueError, match="empty cart"):
        build_order([], products)
    with pytest.raises(KeyError) as captured:
        build_order([("999", 1)], products)
    assert captured.value.args == ("999",)
