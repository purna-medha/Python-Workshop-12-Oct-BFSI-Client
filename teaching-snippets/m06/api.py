# M6/M8 companion: existing contracts/domain operations backed by SQLite.
from fastapi import Depends, FastAPI, HTTPException
from m03.shop import create_order
from m05.adapters import order_response
from m05.contracts import OrderRequest, OrderResponse
from m06.api_dependencies import get_connection
from m06.orders import load_order, save_order
from m06.products import load_products


def create_app(database_path):
    app = FastAPI(title="Teaching shop: persistent orders")
    app.state.database_path = database_path

    @app.post("/orders", response_model=OrderResponse, status_code=201)
    def place_order(request: OrderRequest, connection=Depends(get_connection)):
        try:
            order = create_order([(item.product_id, item.quantity)
                                  for item in request.items], load_products(connection))
        except KeyError as error:
            raise HTTPException(404, "Product not found") from error
        except ValueError as error:
            raise HTTPException(422, str(error)) from error
        save_order(connection, order)
        return order_response(order)

    @app.get("/orders/{order_id}", response_model=OrderResponse)
    def get_order(order_id: str, connection=Depends(get_connection)):
        try:
            return order_response(load_order(connection, order_id))
        except KeyError as error:
            raise HTTPException(404, "Order not found") from error

    return app
