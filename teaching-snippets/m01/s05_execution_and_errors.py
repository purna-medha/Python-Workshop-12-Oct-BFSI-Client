# Execution follows statements and function calls in order. An exception
# interrupts that flow. A traceback records the calls and failing line,
# giving evidence for locating the problem. Local names belong to their call.
#
# Follow quantity text through conversion and calculation. Then change the
# second input to "two" to expose a real conversion traceback.

def parse_quantity(quantity_text):
    quantity = int(quantity_text)
    return quantity


def total_from_input(unit_price_paise, quantity_text):
    quantity = parse_quantity(quantity_text)
    return unit_price_paise * quantity


print(total_from_input(49900, "2"))  # 99800
print(total_from_input(49900, "3"))  # 149700; change "3" to "two".

# Read the exception message and innermost frame, then follow the callers.
# The caller receives the return value, not access to parse_quantity's locals.
# M2 introduces handling of expected input failures.
