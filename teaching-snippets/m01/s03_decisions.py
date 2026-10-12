# Conditions select a path according to a rule. Comparisons produce Boolean
# values; if/elif/else uses those values to choose a block. Rule order matters
# when several conditions could apply. Indentation defines Python's blocks.
#
# Reject invalid purchases before deciding whether delivery is free.

is_available = True
quantity = 2
unit_price_paise = 49900

if not is_available:
    print("Product unavailable")
elif quantity <= 0:
    print("Quantity must be positive")
else:
    subtotal_paise = unit_price_paise * quantity
    if subtotal_paise >= 100000:
        delivery_fee_paise = 0
    else:
        delivery_fee_paise = 5000
    print(f"Subtotal: {subtotal_paise}; delivery: {delivery_fee_paise}")
    print(f"Total: {subtotal_paise + delivery_fee_paise}")

print("Decision complete")         # Outside every conditional block.

# Expected: subtotal 99800, delivery 5000, total 104800.
# Try quantities 3 and 0. Predict the chosen path before running.
