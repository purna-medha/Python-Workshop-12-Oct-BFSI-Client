# Records give related fields a named structure. Dataclasses generate routine
# initialization and representations, making the expected fields explicit.
# Their type hints describe intent rather than validate inputs at runtime.
#
# Products describe catalog facts; cart items pair products with quantities.

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    price_paise: int


@dataclass
class CartItem:
    product: Product
    quantity: int


cable = Product("1", "USB-C Cable", 49900)
item = CartItem(cable, 2)
print(item.product.price_paise * item.quantity)  # 99800
print(asdict(cable))
item.quantity = 3                   # Mutable cart data.
print(item)
# frozen prevents normal Product field reassignment; nested data is not frozen.
