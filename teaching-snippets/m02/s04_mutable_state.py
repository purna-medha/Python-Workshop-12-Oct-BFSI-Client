# Assignment can bind several names to one object; mutation is then visible
# through all those names. A shallow copy creates only a new outer container.
# Independent callers need deliberately separate mutable state.
#
# Compare aliases, copies, and a function that creates a fresh cart per call.

first_cart = ["1"]
another_name = first_cart
another_name.append("3")
print(first_cart)                  # ['1', '3']
copied_cart = first_cart.copy()
print(copied_cart == first_cart)    # True: equal contents.
print(copied_cart is first_cart)    # False: different objects.

records = [{"product_id": "1", "quantity": 1}]
copied_records = records.copy()
copied_records[0]["quantity"] = 2
print(records[0]["quantity"])      # 2: inner dictionary is still shared.


def add_product(product_id, cart=None):
    # Defaults are evaluated once. A default [] would be shared across calls.
    if cart is None:
        cart = []
    cart.append(product_id)
    return cart


print(add_product("1"))            # ['1']
print(add_product("3"))            # ['3']: independent state.
# Try passing first_cart explicitly; the function then changes that cart.
