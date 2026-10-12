# M6 companion: connection ownership and supplied schema initialization.
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from m03.catalog import PRODUCTS


@contextmanager
def connect(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    finally:
        connection.close()


def initialize(connection):
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    connection.executescript(schema)  # Initialize outside an order transaction.
    with connection:
        connection.executemany(
            "INSERT OR IGNORE INTO products VALUES (?, ?, ?)",
            [(p.product_id, p.name, p.price_paise) for p in PRODUCTS.values()],
        )
