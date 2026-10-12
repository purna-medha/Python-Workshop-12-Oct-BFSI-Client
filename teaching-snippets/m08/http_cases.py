# M8 companion: deterministic substitutes for the external HTTP response only.
import requests
from unittest.mock import Mock

PAYLOAD = {"items": [{"product_id": "1", "quantity": 2}]}
RESULT = {
    "order_id": "example-order", "total_paise": 99800,
    "lines": [{"product_id": "1", "name": "USB-C Cable",
               "unit_price_paise": 49900, "quantity": 2}],
}


def response_for(case):
    response = Mock(spec=requests.Response)
    response.raise_for_status.return_value = None
    response.json.return_value = RESULT
    if case == "rejected":
        response.raise_for_status.side_effect = requests.HTTPError("404")
    elif case == "malformed":
        response.json.side_effect = ValueError("Invalid JSON")
    return response
