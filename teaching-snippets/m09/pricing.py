# M9 companion: the same line-total rule used throughout Nano-Zon.
def calculate_line_total(unit_price_paise: int, quantity: int) -> int:
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")
    return unit_price_paise * quantity
