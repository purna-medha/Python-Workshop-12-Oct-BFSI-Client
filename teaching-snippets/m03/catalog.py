# M3 companion: fixed catalog records shared by later examples.
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    price_paise: int


PRODUCTS = {
    "1": Product("1", "USB-C Cable", 49900),
    "2": Product("2", "Mechanical Keyboard", 549900),
    "3": Product("3", "Steel Water Bottle", 89900),
}
