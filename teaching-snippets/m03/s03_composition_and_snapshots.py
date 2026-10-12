# Composition builds larger concepts from smaller records. Historical data
# must preserve its own facts rather than reference mutable working state.
# Fresh defaults and immutable snapshots make those boundaries explicit.
#
# A cart contains mutable items; an order retains checkout-time values.

from dataclasses import dataclass, field


@dataclass
class CartItem:
    product_id: str
    unit_price_paise: int
    quantity: int


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    unit_price_paise: int
    quantity: int


cart = Cart([CartItem("1", 49900, 2)])
order_lines = tuple(OrderLine(item.product_id, item.unit_price_paise, item.quantity)
                    for item in cart.items)
cart.items[0].quantity = 5
print(sum(line.unit_price_paise * line.quantity for line in order_lines))  # 99800
print(Cart().items)                 # []: independent default.
# tuple(cart.items) alone would retain references to mutable CartItem objects.
