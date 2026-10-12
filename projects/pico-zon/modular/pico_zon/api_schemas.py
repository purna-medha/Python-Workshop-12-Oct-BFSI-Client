# External data needs an explicit contract; ordinary annotations alone do
# not establish runtime validity. Product existence remains a shopping rule.
from pydantic import BaseModel, ConfigDict, Field


class ProductResponse(BaseModel):
    product_id: str
    name: str
    price_paise: int = Field(strict=True, ge=0)


class RequestedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: str = Field(strict=True, min_length=1)
    quantity: int = Field(strict=True, gt=0)


class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[RequestedItem] = Field(min_length=1)


class OrderLineResponse(BaseModel):
    product_id: str
    name: str
    unit_price_paise: int = Field(strict=True, ge=0)
    quantity: int = Field(strict=True, gt=0)


class OrderResponse(BaseModel):
    order_id: str
    lines: list[OrderLineResponse] = Field(min_length=1)
    total_paise: int = Field(strict=True, ge=0)
