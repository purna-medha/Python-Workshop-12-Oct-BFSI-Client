# Persistent data outlives a connection. Resource lifetime must be managed:
# SQLite's connection context commits or rolls back, but does not close it.
# Parameterized SQL keeps values separate from SQL structure.
#
# Save a product, close the connection, then reopen the same database file.

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    database_path = Path(directory) / "shop.sqlite"
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute(
                "CREATE TABLE products (product_id TEXT PRIMARY KEY, price_paise INTEGER)",
            )
            connection.execute("INSERT INTO products VALUES (?, ?)", ("1", 49900))
            connection.execute(
                "UPDATE products SET price_paise = ? WHERE product_id = ?",
                (50000, "1"),
            )
    with closing(sqlite3.connect(database_path)) as connection:
        row = connection.execute(
            "SELECT price_paise FROM products WHERE product_id = ?", ("1",),
        ).fetchone()
        print(row[0])              # 50000: survives the first connection closing.
# TemporaryDirectory removes only this demonstration's database at the end.
# Use a chosen lasting path when information must survive the program itself.
