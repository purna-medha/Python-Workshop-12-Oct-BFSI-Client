# One caller process uses the public interface, independent of server objects.
import os
import requests
from .client import get_order, list_products, submit_order


def main():
    base_url = os.getenv("NANOZON_API_URL", "http://127.0.0.1:8000")
    try:
        print(list_products(base_url, query="cable"))
        order = submit_order(base_url, {"items": [{"product_id": "1", "quantity": 2}]})
        print(order.total_paise)
        print(get_order(base_url, order.order_id))
    except requests.HTTPError as error:
        print("HTTP rejection:", error.response.status_code)
    except requests.exceptions.JSONDecodeError as error:
        print("Invalid JSON response:", error)
    except requests.RequestException as error:
        print("Communication failure:", error)
    except ValueError as error:
        print("Invalid response:", error)


if __name__ == "__main__":
    main()
