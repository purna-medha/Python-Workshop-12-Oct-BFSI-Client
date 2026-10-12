# Collections support lookup and selection; queries leave supplied records unchanged.
from .models import Product


def seed_products() -> dict[str, Product]:
    return {
        "1": Product("1", "USB-C Cable", "Electronics", 49900),
        "2": Product("2", "Mechanical Keyboard", "Electronics", 549900),
        "3": Product("3", "Steel Water Bottle", "Home", 89900),
    }


def select_products(products, *, query="", minimum_paise=None, maximum_paise=None):
    for bound in (minimum_paise, maximum_paise):
        if bound is not None and (type(bound) is not int or bound < 0):
            raise ValueError("Price bounds must be non-negative integers")
    if minimum_paise is not None and maximum_paise is not None:
        if minimum_paise > maximum_paise:
            raise ValueError("Minimum price cannot exceed maximum price")
    normalized_query = query.strip().casefold()
    matches = []
    for product in products.values():
        if normalized_query not in product.name.casefold():
            continue
        if minimum_paise is not None and product.price_paise < minimum_paise:
            continue
        if maximum_paise is not None and product.price_paise > maximum_paise:
            continue
        matches.append(product)
    return sorted(matches, key=lambda product: product.product_id)
