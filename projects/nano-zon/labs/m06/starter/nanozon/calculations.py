# Values and functions express reusable operations, independently of display or HTTP.

def validate_quantity(quantity: int) -> None:
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")


def money(paise: int) -> str:
    return f"₹{paise // 100}.{paise % 100:02d}"


def calculate_line_total(unit_price_paise: int, quantity: int) -> int:
    validate_quantity(quantity)
    return unit_price_paise * quantity
