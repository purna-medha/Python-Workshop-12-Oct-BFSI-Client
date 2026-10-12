# Expressions combine values to produce new values. The representation
# affects the calculation: integer minor units keep monetary arithmetic
# exact. Formatting changes how a result is displayed, not how it is stored.
#
# Calculate two cables, then display their total in rupees and paise.

unit_price_paise = 49900
quantity = int("2")
line_total_paise = unit_price_paise * quantity
whole_rupees = line_total_paise // 100
remaining_paise = line_total_paise % 100
display_total = f"₹{whole_rupees}.{remaining_paise:02d}"

print(line_total_paise)            # 99800
print(display_total)               # ₹998.00
print(line_total_paise >= 100000)   # False: comparisons produce booleans.
print("2" * 3)                     # 222: string repetition, not multiplication.

product_name = "  USB-C Cable  "
print(product_name.strip().lower())

# Try a price of 49950. The stored total and formatted total must agree.
