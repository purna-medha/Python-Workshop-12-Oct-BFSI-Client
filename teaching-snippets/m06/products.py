# M6 companion: translate database rows into the existing domain records.
from m03.catalog import Product


def load_products(connection):
    rows = connection.execute(
        "SELECT product_id, name, price_paise FROM products ORDER BY product_id",
    ).fetchall()
    return {row["product_id"]: Product(**dict(row)) for row in rows}
