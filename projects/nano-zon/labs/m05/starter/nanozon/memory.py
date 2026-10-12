# M3–M5 storage keeps orders for one process; it has the same small interface as SQLite.
from .catalog import seed_products


class MemoryStore:
    def __init__(self):
        self.products = seed_products()
        self.orders = {}

    def all_products(self):
        return dict(self.products)

    def save_order(self, order):
        if order.order_id in self.orders:
            raise ValueError("Order ID already exists")
        self.orders[order.order_id] = order

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise KeyError(order_id)
        return self.orders[order_id]
