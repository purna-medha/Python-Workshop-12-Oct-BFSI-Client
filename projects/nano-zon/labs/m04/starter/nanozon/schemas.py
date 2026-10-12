# M4: dataclass input; explicit constraints arrive in M5.
from dataclasses import dataclass


@dataclass
class RequestedItem:
    product_id: str
    quantity: int


@dataclass
class OrderRequest:
    items: list[RequestedItem]


@dataclass
class OrderResponse:
    order_id: str
    lines: list[dict]
    total_paise: int
