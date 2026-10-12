# Missing information, valid empty values, and invalid inputs differ.
# A function raises a specific exception when it cannot fulfill its contract;
# the interaction layer handles that expected failure and chooses what follows.
# Catching unrelated failures would conceal programming defects.
#
# Retry invalid quantities, then accept a positive one. Inputs are simulated.

def parse_positive_quantity(quantity_text):
    quantity = int(quantity_text)
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    return quantity


attempted_inputs = iter(["two", "0", "2"])
while True:
    try:
        quantity = parse_positive_quantity(next(attempted_inputs))
    except ValueError as error:
        print(f"Try again: {error}")
        continue
    print(f"Accepted: {quantity}")
    break

cart = []
if not cart:
    print("Empty cart")             # Truthiness fits an empty collection.
maximum_price_paise = 0
if maximum_price_paise is not None:
    print("Apply bound:", maximum_price_paise)
# if maximum_price_paise would wrongly ignore zero. A real CLI uses input().
