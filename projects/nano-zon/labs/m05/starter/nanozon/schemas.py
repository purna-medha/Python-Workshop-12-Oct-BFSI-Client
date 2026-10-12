# Boundary contracts validate external data; product existence stays in domain logic.
from pydantic import BaseModel, ConfigDict, Field


class ProductResponse(BaseModel):
    product_id: str
    name: str
    category: str
    price_paise: int = Field(strict=True, ge=0)


class RequestedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: str = Field(min_length=1, strict=True)
    # ANSWER m05 quantity_contract BEGIN
    # quantity: int = Field(strict=True, gt=0)
    quantity: int  # LAB-GUARD: remove when answering
    # ANSWER m05 quantity_contract END


class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # ANSWER m05 nonempty_contract BEGIN
    # items: list[RequestedItem] = Field(min_length=1)
    items: list[RequestedItem]  # LAB-GUARD: remove when answering
    # ANSWER m05 nonempty_contract END


class OrderLineResponse(BaseModel):
    product_id: str
    name: str
    unit_price_paise: int = Field(strict=True, ge=0)
    quantity: int = Field(strict=True, gt=0)


class OrderResponse(BaseModel):
    order_id: str
    lines: list[OrderLineResponse] = Field(min_length=1)
    total_paise: int = Field(strict=True, ge=0)
