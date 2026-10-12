# An instance owns each shopper's mutable selection. Repeated IDs represent
# repeated units, just as they do in the monolithic opening application.
from .catalog import get_product


class ShoppingCart:
    def __init__(self):
        self.product_ids: list[str] = []

    def add(self, product_id: str, quantity: int = 1) -> None:
        get_product(product_id)
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.product_ids.extend([product_id] * quantity)

    def clear(self) -> None:
        self.product_ids.clear()

    @property
    def subtotal_paise(self) -> int:
        return sum(get_product(product_id).price_paise
                   for product_id in self.product_ids)
