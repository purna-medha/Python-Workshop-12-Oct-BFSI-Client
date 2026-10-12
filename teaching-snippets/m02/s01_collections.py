# Collections support different access patterns: lists preserve sequences,
# dictionaries associate keys with values, tuples group fixed sequences,
# and sets represent unique membership. Choose according to the operation.
#
# Look products up by ID, retain repeated selections, and list unique categories.

products = {
    "1": {"name": "USB-C Cable", "category": "Electronics", "price_paise": 49900},
    "2": {"name": "Mechanical Keyboard", "category": "Electronics", "price_paise": 549900},
    "3": {"name": "Steel Water Bottle", "category": "Home", "price_paise": 89900},
}
selected_ids = ["1", "3", "1"]
product_and_quantity = ("1", 2)
categories = {"Electronics", "Home", "Electronics"}

print(products["1"]["name"])
print(selected_ids[0])
product_id, quantity = product_and_quantity  # Tuple unpacking.
print(product_id, quantity)
print(sorted(categories))          # A set has no promised display order.
print("2" in products)             # Dictionary membership checks keys.
print(products.get("missing"))     # None rather than a KeyError.

# List repetition retains units; set repetition adds no extra category.
