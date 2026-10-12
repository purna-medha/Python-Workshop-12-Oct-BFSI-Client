# Records give related facts named shapes. Orders retain immutable purchase facts.
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    category: str
    price_paise: int


@dataclass(frozen=True)
class CartItem:
    product: Product
    quantity: int


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    name: str
    unit_price_paise: int
    quantity: int

    @property
    def line_total_paise(self) -> int:
        return self.unit_price_paise * self.quantity


@dataclass(frozen=True)
class Order:
    order_id: str
    lines: tuple[OrderLine, ...]

    @property
    def total_paise(self) -> int:
        return sum(line.line_total_paise for line in self.lines)

    def to_dict(self) -> dict:
        return {**asdict(self), "total_paise": self.total_paise}
