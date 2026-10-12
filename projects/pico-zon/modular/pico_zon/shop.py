# Checkout expresses the shopping rule, independently of terminal or HTTP.
# Construct new line records; save successfully before clearing working state.
from uuid import uuid4
from .cart import ShoppingCart
from .catalog import get_product
from .models import Order, OrderLine


def checkout(cart: ShoppingCart, store=None) -> Order:
    if not cart.product_ids:
        raise ValueError("Your cart is empty.")
    products = [get_product(product_id) for product_id in cart.product_ids]
    order = Order(uuid4().hex, tuple(
        OrderLine(product.product_id, product.name, product.price_paise)
        for product in products
    ))
    if store is not None:
        store.save_order(order)
    cart.clear()
    return order
