# Programs represent facts using values. Types determine which operations
# make sense; names explain what each value means in the problem. Assignment
# binds a name to a value rather than giving the name a permanent type.
#
# Describe a product. An absent description differs from an empty string.

product_name = "USB-C Cable"       # str: text
unit_price_paise = 49900           # int: whole-number money units
shipping_weight_kg = 0.08          # float: approximate measurement
is_available = True               # bool: a true/false fact
description = None                # NoneType: an absent value

print(product_name)
print(type(unit_price_paise).__name__)
print(type(shipping_weight_kg).__name__)
print(is_available)
print(description is None)

shopper_input = "2"
quantity = int(shopper_input)      # Explicitly convert text to a number.
print(type(shopper_input).__name__, type(quantity).__name__)

# Expected: USB-C Cable, int, float, True, True, then str int.
# Try: compare None and "". What could each mean in another application?
