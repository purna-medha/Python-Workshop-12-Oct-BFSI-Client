# M3 companion: immutable purchase records, distinct from mutable cart state.
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    name: str
    unit_price_paise: int
    quantity: int


@dataclass(frozen=True)
class Order:
    order_id: str
    lines: tuple[OrderLine, ...]

    @property
    def total_paise(self) -> int:
        return sum(line.unit_price_paise * line.quantity for line in self.lines)
