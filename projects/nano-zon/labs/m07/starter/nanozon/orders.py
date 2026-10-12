# Checkout creates an independent snapshot; later cart/catalog changes cannot rewrite it.
from uuid import uuid4
from .calculations import validate_quantity
from .models import Order, OrderLine


def build_order(items: list[tuple[str, int]], products) -> Order:
    if not items:
        raise ValueError("Cannot checkout an empty cart")
    lines = []
    for product_id, quantity in items:
        validate_quantity(quantity)
        if product_id not in products:
            raise KeyError(product_id)
        product = products[product_id]
        # ANSWER m03 snapshot BEGIN
        lines.append(OrderLine(
            product_id=product.product_id,
            name=product.name,
            unit_price_paise=product.price_paise,
            quantity=quantity,
        ))
        # ANSWER m03 snapshot END
    return Order(uuid4().hex, tuple(lines))
