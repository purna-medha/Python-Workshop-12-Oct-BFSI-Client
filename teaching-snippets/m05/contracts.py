# M5 companion: explicit request/response contracts reused by APIs and callers.
from pydantic import BaseModel, ConfigDict, Field


class RequestedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: str = Field(min_length=1, strict=True)
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
