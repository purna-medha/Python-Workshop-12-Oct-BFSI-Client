# Persistence translates records and groups related writes into one transaction.
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from .catalog import seed_products
from .models import Order, OrderLine, Product


class SQLiteStore:
    def __init__(self, database_path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self):
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self.connect() as connection:
            connection.executescript(schema)
            with connection:
                connection.executemany("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)",
                                       [(p.product_id, p.name, p.category, p.price_paise)
                                        for p in seed_products().values()])

    def all_products(self):
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT product_id, name, category, price_paise FROM products ORDER BY product_id",
            ).fetchall()
        # ANSWER m06 row_conversion BEGIN
        return {row["product_id"]: Product(**dict(row)) for row in rows}
        # ANSWER m06 row_conversion END

    def save_order(self, order):
        with self.connect() as connection:
            # ANSWER m06 atomic_save BEGIN
            with connection:
                connection.execute("INSERT INTO orders VALUES (?, ?)",
                                   (order.order_id, order.total_paise))
                for position, line in enumerate(order.lines):
                    connection.execute("INSERT INTO order_lines VALUES (?, ?, ?, ?, ?, ?)",
                                       (order.order_id, position, line.product_id, line.name,
                                        line.unit_price_paise, line.quantity))
            # ANSWER m06 atomic_save END

    def get_order(self, order_id):
        with self.connect() as connection:
            header = connection.execute("SELECT total_paise FROM orders WHERE order_id = ?",
                                        (order_id,)).fetchone()
            if header is None:
                raise KeyError(order_id)
            # ANSWER m06 parameterized_lookup BEGIN
            rows = connection.execute(
                "SELECT product_id, name, unit_price_paise, quantity FROM order_lines "
                "WHERE order_id = ? ORDER BY line_number", (order_id,),
            ).fetchall()
            # ANSWER m06 parameterized_lookup END
        # ANSWER m06 reconstruct_order BEGIN
        order = Order(order_id, tuple(OrderLine(**dict(row)) for row in rows))
        if order.total_paise != header["total_paise"]:
            raise ValueError("Stored order total does not match its lines")
        return order
        # ANSWER m06 reconstruct_order END
