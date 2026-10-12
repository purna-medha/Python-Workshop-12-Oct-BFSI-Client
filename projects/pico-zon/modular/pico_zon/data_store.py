# Persistence extends information's lifetime. A single order document keeps
# this showcase small; Nano-Zon teaches normalized headers and order lines.
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from .models import Order


class SQLiteStore:
    def __init__(self, database_path):
        self.database_path = Path(database_path)

    def initialize(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS orders "
                    "(order_id TEXT PRIMARY KEY, document TEXT NOT NULL)",
                )

    def save_order(self, order: Order):
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                connection.execute("INSERT INTO orders VALUES (?, ?)",
                                   (order.order_id, json.dumps(order.to_dict())))

    def get_order(self, order_id: str) -> dict:
        with closing(sqlite3.connect(self.database_path)) as connection:
            row = connection.execute("SELECT document FROM orders WHERE order_id = ?",
                                     (order_id,)).fetchone()
        if row is None:
            raise KeyError(order_id)
        return json.loads(row[0])
