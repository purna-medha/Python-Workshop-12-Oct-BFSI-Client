# Catalog lookup is shared by every interface; display belongs to the caller.
from .models import Product

PRODUCTS = {
    "1": Product("1", "USB-C Cable", 49900),
    "2": Product("2", "Mechanical Keyboard", 549900),
    "3": Product("3", "Steel Water Bottle", 89900),
}


def list_products(query: str = "") -> list[Product]:
    return [product for product in PRODUCTS.values()
            if query.casefold() in product.name.casefold()]


def get_product(product_id: str) -> Product:
    if product_id not in PRODUCTS:
        raise KeyError(product_id)
    return PRODUCTS[product_id]
