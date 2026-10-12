# Functions name an operation and separate its implementation from callers.
# Parameters describe required inputs; arguments supply values at a call.
# Returning a value lets the caller choose how to use or display the result.
#
# Calculate different cart lines with the same operation, then combine them.

def calculate_line_total(unit_price_paise, quantity):
    return unit_price_paise * quantity


cable_total_paise = calculate_line_total(49900, 2)
bottle_total_paise = calculate_line_total(
    unit_price_paise=89900, quantity=3,
)
print(cable_total_paise + bottle_total_paise)  # 369500


def display_line_total(unit_price_paise, quantity):
    print(unit_price_paise * quantity)


displayed_result = display_line_total(49900, 2)
print(displayed_result)            # None: printing does not return a total.

# Try the same function pattern for distance = speed * duration.
