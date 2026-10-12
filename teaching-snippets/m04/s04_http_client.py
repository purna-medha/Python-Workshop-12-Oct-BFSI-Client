# A remote call has several possible outcomes: communication fails, the server
# rejects the request, or a successful response contains data to interpret.
# Explicit timeouts bound waiting; status checking precedes reading success data.
#
# Start M4 snippet 03's API first. This caller browses, orders, and retrieves.

import requests

base_url = "http://127.0.0.1:8000"
try:
    catalog_response = requests.get(f"{base_url}/products", timeout=5)
    catalog_response.raise_for_status()
    print(catalog_response.json())
    order_response = requests.post(
        f"{base_url}/orders",
        json={"items": [{"product_id": "1", "quantity": 2}]},
        timeout=5,
    )
    order_response.raise_for_status()
    order = order_response.json()
    print(order["total_paise"])      # 99800
    saved_response = requests.get(
        f"{base_url}/orders/{order['order_id']}", timeout=5,
    )
    saved_response.raise_for_status()
    print(saved_response.json()["order_id"])
except requests.HTTPError as error:
    print("HTTP rejection:", error.response.status_code)
except requests.exceptions.JSONDecodeError as error:
    print("Invalid JSON response:", error)
except requests.RequestException as error:
    print("Communication failure:", error)
except ValueError as error:
    print("Invalid JSON response:", error)
# Try an unknown ID, then stop the server. The failure categories differ.
