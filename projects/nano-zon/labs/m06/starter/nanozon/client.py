# Remote calls separate transport, HTTP rejection, JSON decoding, and response shape.
import requests
from pydantic import TypeAdapter
from .schemas import OrderResponse, ProductResponse


def list_products(base_url: str, query: str = "") -> list[ProductResponse]:
    response = requests.get(f"{base_url.rstrip('/')}/products",
                            params={"query": query}, timeout=5)
    response.raise_for_status()
    return TypeAdapter(list[ProductResponse]).validate_python(response.json())


def submit_order(base_url: str, payload: dict) -> OrderResponse:
    # ANSWER m04 client_call BEGIN
    response = requests.post(f"{base_url.rstrip('/')}/orders", json=payload, timeout=5)
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())
    # ANSWER m04 client_call END


def get_order(base_url: str, order_id: str) -> OrderResponse:
    response = requests.get(f"{base_url.rstrip('/')}/orders/{order_id}", timeout=5)
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())
