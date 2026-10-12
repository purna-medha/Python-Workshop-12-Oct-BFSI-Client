# Modules group definitions by responsibility. Separating domain operations
# from interaction lets a terminal, API, and tests reuse the same behavior.
# Importing definitions should not start an interactive program as a side effect.
#
# Read catalog.py, records.py, shop.py, and cart.py here as small companions.
# cli.py demonstrates presentation; these imports demonstrate reuse.

from m03.cart import ShoppingCart
from m03.shop import calculate_line_total


def main():
    cart = ShoppingCart()
    cart.add("1", 2)
    cart.add("3")
    order = cart.checkout()
    print(f"Order total: {order.total_paise} paise")  # 189700
    print(f"Cart after checkout: {cart.quantities}")
    print(calculate_line_total(49900, 2))


if __name__ == "__main__":
    main()

# Launch from current-course/teaching-snippets: python -m m03.s04_modules
# A class owns state; a stateless calculation can remain an ordinary function.
