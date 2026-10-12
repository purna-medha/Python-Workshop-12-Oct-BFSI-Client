# M3 companion: cart ownership delegates checkout to the domain operation.
from m03.catalog import PRODUCTS
from m03.shop import calculate_line_total, create_order


class ShoppingCart:
    def __init__(self):
        self.quantities: dict[str, int] = {}

    def add(self, product_id: str, quantity: int = 1):
        if product_id not in PRODUCTS:
            raise KeyError(product_id)
        calculate_line_total(PRODUCTS[product_id].price_paise, quantity)
        self.quantities[product_id] = self.quantities.get(product_id, 0) + quantity

    def checkout(self):
        order = create_order(list(self.quantities.items()))
        self.quantities.clear()    # Change state only after successful creation.
        return order
