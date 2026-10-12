# Related records use stable identities to connect information. Historical
# records must retain the facts that applied when they were created, even if
# current data changes. Storage operations translate these records consistently.
#
# Save an order and its lines, change the catalog price, and retrieve the order.

from pathlib import Path
from tempfile import TemporaryDirectory
from m03.shop import create_order
from m06.database import connect, initialize
from m06.orders import load_order, save_order
from m06.products import load_products

with TemporaryDirectory() as directory:
    database_path = Path(directory) / "shop.sqlite"
    with connect(database_path) as connection:
        initialize(connection)
        order = create_order([("1", 2)], load_products(connection))
        save_order(connection, order)
        with connection:
            connection.execute(
                "UPDATE products SET price_paise = ? WHERE product_id = ?",
                (99900, "1"),
            )
    with connect(database_path) as connection:
        saved_order = load_order(connection, order.order_id)
        print(saved_order.lines[0].unit_price_paise)  # 49900: snapshot price.
        print(saved_order.total_paise)               # 99800, not 199800.
# Inspect schema.sql and orders.py: identity joins records; snapshots retain facts.
