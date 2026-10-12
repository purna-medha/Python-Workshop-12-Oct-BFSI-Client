# Boundary handlers translate requests and delegate rules to reusable operations.
# Requests express intentions; the server calculates authoritative prices.
# Add order creation and retrieval to the catalog API using dataclass input.

from dataclasses import asdict, dataclass
from fastapi import HTTPException
from m03.shop import create_order
from m04.s02_catalog_api import app

orders = {}                        # Demonstration state; lost on restart.

@dataclass
class RequestedItem:
    product_id: str
    quantity: int


@dataclass
class OrderRequest:
    items: list[RequestedItem]

@app.post("/orders", status_code=201)
def place_order(request: OrderRequest):
    try:
        order = create_order([(item.product_id, item.quantity) for item in request.items])
    except KeyError as error:
        raise HTTPException(404, "Product not found") from error
    except ValueError as error:
        raise HTTPException(422, str(error)) from error
    orders[order.order_id] = {**asdict(order), "total_paise": order.total_paise}
    return orders[order.order_id]


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(404, "Order not found")
    return orders[order_id]

# Launch: uv run uvicorn m04.s03_order_api:app --port 8000 (stop the previous API).
