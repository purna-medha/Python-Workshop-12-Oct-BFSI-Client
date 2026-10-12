# A remote call checks HTTP success, decodes JSON, and validates order shape.
import requests
from pydantic import TypeAdapter
from .api_schemas import OrderResponse, ProductResponse


def list_products(base_url: str) -> list[ProductResponse]:
    response = requests.get(f"{base_url.rstrip('/')}/products", timeout=5)
    response.raise_for_status()
    return TypeAdapter(list[ProductResponse]).validate_python(response.json())


def submit_order(base_url: str, payload: dict) -> OrderResponse:
    response = requests.post(f"{base_url.rstrip('/')}/orders", json=payload, timeout=5)
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())


def get_order(base_url: str, order_id: str) -> OrderResponse:
    response = requests.get(f"{base_url.rstrip('/')}/orders/{order_id}", timeout=5)
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())
