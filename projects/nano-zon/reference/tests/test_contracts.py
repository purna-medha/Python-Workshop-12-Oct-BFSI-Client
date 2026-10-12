# Supplied M5 checks make input policies visible when test authoring begins in M7.
import pytest
from pydantic import ValidationError
from nanozon.schemas import OrderRequest


@pytest.mark.parametrize("quantity", [0, -1, True, "2", 1.5])
def test_quantity_contract_rejects_unsuitable_values(quantity):
    with pytest.raises(ValidationError):
        OrderRequest(items=[{"product_id": "1", "quantity": quantity}])


def test_empty_request_and_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        OrderRequest(items=[])
    with pytest.raises(ValidationError):
        OrderRequest(items=[{"product_id": "1", "quantity": 2}], total_paise=1)
