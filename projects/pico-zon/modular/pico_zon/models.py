# Records give related facts names. Orders retain purchase-time values,
# independently of the cart that produced them.
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    price_paise: int


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    name: str
    unit_price_paise: int
    quantity: int = 1


@dataclass(frozen=True)
class Order:
    order_id: str
    lines: tuple[OrderLine, ...]

    @property
    def total_paise(self) -> int:
        return sum(line.unit_price_paise * line.quantity for line in self.lines)

    def to_dict(self) -> dict:
        return {**asdict(self), "total_paise": self.total_paise}
