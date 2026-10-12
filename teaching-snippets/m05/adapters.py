# M5 companion: translate domain records into the external response contract.
from dataclasses import asdict
from m05.contracts import OrderResponse


def order_response(order) -> OrderResponse:
    return OrderResponse(**asdict(order), total_paise=order.total_paise)
