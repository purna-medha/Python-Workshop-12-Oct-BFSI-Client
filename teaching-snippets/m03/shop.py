# M3 companion: ordinary business functions, independent of display and HTTP.
from uuid import uuid4
from m03.catalog import PRODUCTS
from m03.records import Order, OrderLine


def calculate_line_total(unit_price_paise: int, quantity: int) -> int:
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")
    return unit_price_paise * quantity


def create_order(items: list[tuple[str, int]], products=None) -> Order:
    catalog = PRODUCTS if products is None else products
    if not items:
        raise ValueError("Cannot checkout an empty cart")
    lines = []
    for product_id, quantity in items:
        if product_id not in catalog:
            raise KeyError(product_id)
        product = catalog[product_id]
        calculate_line_total(product.price_paise, quantity)
        lines.append(OrderLine(product_id, product.name, product.price_paise, quantity))
    return Order(uuid4().hex, tuple(lines))
