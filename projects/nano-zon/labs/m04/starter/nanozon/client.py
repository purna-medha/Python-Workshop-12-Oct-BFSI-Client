# Remote calls separate transport, HTTP rejection, JSON decoding, and response shape.
import requests


def list_products(base_url: str, query: str = "") -> list[dict]:
    response = requests.get(f"{base_url.rstrip('/')}/products",
                            params={"query": query}, timeout=5)
    response.raise_for_status()
    return response.json()


def submit_order(base_url: str, payload: dict) -> dict:
    # ANSWER m04 client_call BEGIN
    # response = requests.post(f"{base_url.rstrip('/')}/orders", json=payload, timeout=5)
    # response.raise_for_status()
    # return response.json()
    raise NotImplementedError("M04: complete client_call")  # LAB-GUARD: remove when answering
    # ANSWER m04 client_call END


def get_order(base_url: str, order_id: str) -> dict:
    response = requests.get(f"{base_url.rstrip('/')}/orders/{order_id}", timeout=5)
    response.raise_for_status()
    return response.json()
