# Function interfaces distinguish required inputs from optional choices.
# Names, defaults, documentation, and type hints communicate the contract.
# Type hints help readers and tools; they do not enforce types at runtime.
#
# Search a catalog using optional named filters without changing its records.

def search_products(
    products: list[dict], *, query: str = "",
    maximum_price_paise: int | None = None,
) -> list[dict]:
    """Return matches; leave the supplied catalog unchanged."""
    normalized_query = query.strip().casefold()
    matches = []
    for product in products:
        if normalized_query not in product["name"].casefold():
            continue
        if maximum_price_paise is not None:
            if product["price_paise"] > maximum_price_paise:
                continue
        matches.append(product)
    return matches


catalog = [{"name": "USB-C Cable", "price_paise": 49900}]
print(search_products(catalog, query="CABLE"))
print(search_products(catalog, maximum_price_paise=0))  # []: zero is a bound.

# * makes the filters keyword-only. normalized_query is local to each call.
# Optional: *args collects extra positional inputs; **kwargs collects named ones.
