# An object owns changing state; composition keeps the cart and product records distinct.
from .calculations import calculate_line_total, validate_quantity
from .catalog import seed_products
from .models import CartItem
from .orders import build_order


class ShoppingCart:
    def __init__(self, products=None):
        self.products = dict(seed_products() if products is None else products)
        self.items: dict[str, CartItem] = {}

    def add(self, product_id: str, quantity: int = 1) -> None:
        validate_quantity(quantity)
        if product_id not in self.products:
            raise KeyError(product_id)
        # ANSWER m03 own_state BEGIN
        # previous = self.items.get(product_id)
        # previous_quantity = 0 if previous is None else previous.quantity
        # self.items[product_id] = CartItem(
        #     self.products[product_id], previous_quantity + quantity,
        # )
        raise NotImplementedError("M03: complete own_state")  # LAB-GUARD: remove when answering
        # ANSWER m03 own_state END

    def update(self, product_id: str, quantity: int) -> None:
        validate_quantity(quantity)
        if product_id not in self.items:
            raise KeyError(product_id)
        self.items[product_id] = CartItem(self.items[product_id].product, quantity)

    def remove(self, product_id: str) -> None:
        if product_id not in self.items:
            raise KeyError(product_id)
        del self.items[product_id]

    @property
    def subtotal_paise(self) -> int:
        # ANSWER m03 subtotal BEGIN
        # return sum(calculate_line_total(item.product.price_paise, item.quantity)
        #            for item in self.items.values())
        raise NotImplementedError("M03: complete subtotal")  # LAB-GUARD: remove when answering
        # ANSWER m03 subtotal END

    def request_items(self) -> list[tuple[str, int]]:
        return [(product_id, item.quantity) for product_id, item in self.items.items()]

    def clear(self) -> None:
        self.items.clear()

    def checkout(self, store):
        order = build_order(self.request_items(), store.all_products())
        store.save_order(order)
        self.clear()               # A failed save leaves the working cart intact.
        return order
