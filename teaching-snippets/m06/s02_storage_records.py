# Database rows and application records serve different purposes. An explicit
# translation keeps SQL details in storage code while the rest of the program
# continues to use meaningful domain records and operations.
#
# Read the supplied schema and database.py; convert one stored product to Product.

from m03.catalog import Product
from m06.database import connect, initialize

with connect(":memory:") as connection:
    initialize(connection)
    row = connection.execute(
        "SELECT product_id, name, price_paise FROM products WHERE product_id = ?",
        ("1",),
    ).fetchone()
    product = Product(
        product_id=row["product_id"],
        name=row["name"],
        price_paise=row["price_paise"],
    )
    print(product.name, product.price_paise)  # USB-C Cable 49900

# fetchone returns None when there is no match; handle absence before conversion.
# m06/products.py applies this same conversion to the complete stored catalog.
