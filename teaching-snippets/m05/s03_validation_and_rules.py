# Structural validation establishes acceptable input shape; business rules
# depend on application facts. A correctly shaped request can reference a
# missing resource. Convert boundary data and delegate that decision to the domain.
#
# Strengthen M4's existing {"items": [...]} contract with explicit constraints.

from fastapi import FastAPI, HTTPException
from m03.shop import create_order
from m05.adapters import order_response
from m05.contracts import OrderRequest, OrderResponse

app = FastAPI(title="Teaching shop: validated input")


@app.post("/orders", response_model=OrderResponse, status_code=201)
def place_order(request: OrderRequest):
    try:
        order = create_order([(item.product_id, item.quantity)
                              for item in request.items])
    except KeyError as error:
        raise HTTPException(404, "Product not found") from error
    except ValueError as error:
        raise HTTPException(422, str(error)) from error
    return order_response(order)


# Launch: uv run uvicorn m05.s03_validation_and_rules:app --port 8000
# In /docs, quantity 0 fails the contract (422); ID "999" fails the domain (404).
# Stop the M4 server first. The request shape stays the same; constraints change.
