# A data contract declares the shape and constraints accepted at a boundary.
# Runtime validation turns untrusted values into data with known properties.
# Explicit models also make the accepted interface visible to other developers.
#
# Require at least one requested item and a positive integer quantity.

from pydantic import BaseModel, Field, ValidationError


class RequestedItem(BaseModel):
    product_id: str
    quantity: int = Field(strict=True, gt=0)


class OrderRequest(BaseModel):
    items: list[RequestedItem] = Field(min_length=1)


request = OrderRequest.model_validate({
    "items": [{"product_id": "1", "quantity": 2}],
})
print(request.items[0].quantity)
print(request.model_dump())
print(OrderRequest.model_validate_json(request.model_dump_json()))

try:
    OrderRequest(items=[{"product_id": "1", "quantity": 0}])
except ValidationError as error:
    print(error.errors()[0]["loc"])  # ('items', 0, 'quantity')
# This contract knows nothing about which products currently exist.
