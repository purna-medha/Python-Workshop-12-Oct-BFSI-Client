# M5 companion: one external HTTP boundary, reused by the workflow and M8 tests.
import requests
from m05.contracts import OrderResponse


def submit_order(base_url: str, payload: dict) -> OrderResponse:
    response = requests.post(
        f"{base_url.rstrip('/')}/orders", json=payload, timeout=5,
    )
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())
