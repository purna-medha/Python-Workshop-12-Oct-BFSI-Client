# Iteration applies an operation across inputs. An accumulator combines
# results, filtering selects elements, and sorting orders them. A comprehension
# expresses a simple selection concisely once its loop form is understood.
#
# Browse products, total selections, and display affordable products by price.

products = {
    "1": {"name": "USB-C Cable", "price_paise": 49900},
    "2": {"name": "Mechanical Keyboard", "price_paise": 549900},
    "3": {"name": "Steel Water Bottle", "price_paise": 89900},
}
for product_id, product in products.items():
    print(product_id, product["name"])

subtotal_paise = 0
for product_id in ["1", "1", "3"]:
    subtotal_paise += products[product_id]["price_paise"]
print(subtotal_paise)               # 189700

affordable = []
for product in products.values():
    if product["price_paise"] <= 100000:
        affordable.append(product)
concise = [p for p in products.values() if p["price_paise"] <= 100000]
print(affordable == concise)        # True: same selection rule.

def price_key(product):
    return product["price_paise"]

for position, product in enumerate(sorted(affordable, key=price_key), start=1):
    print(position, product["name"])

# Try a smaller budget. An empty selection is a valid result.
