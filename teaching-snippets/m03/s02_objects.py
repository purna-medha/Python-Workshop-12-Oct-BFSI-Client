# Objects combine state with operations responsible for changing it. self
# identifies the instance receiving a call. Instance attributes can own fresh
# mutable data; class attributes are shared unless an instance shadows them.
#
# Each shopping cart owns its quantities and checks the rule for adding units.

class ShoppingCart:
    label = "Shopping cart"        # Shared descriptive class data.

    def __init__(self):
        self.quantities = {}       # Fresh dictionary for every instance.

    def add(self, product_id, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        previous = self.quantities.get(product_id, 0)
        self.quantities[product_id] = previous + quantity

    def quantity_for(self, product_id):
        return self.quantities.get(product_id, 0)


first_cart = ShoppingCart()
second_cart = ShoppingCart()
first_cart.add("1", 2)
first_cart.add("1")
print(first_cart.quantity_for("1"))  # 3
print(second_cart.quantity_for("1")) # 0
# Moving quantities = {} into the class body would share the mutable dictionary.
