# HTTP handlers translate requests into domain operations and deliberate responses.
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from .catalog import select_products
from .models import Product
from .orders import build_order
from .schemas import OrderRequest, OrderResponse


def create_app(store):
    app = FastAPI(title="Nano-Zon", description="Simulated orders; no real payments")
    app.state.store = store

    @app.exception_handler(NotImplementedError)
    async def pending_lab(request, error):
        return JSONResponse(status_code=501, content={"detail": str(error)})

    @app.get("/products", response_model=list[Product])
    def list_products(query: str = "", minimum_paise: int | None = Query(None, ge=0),
                      maximum_paise: int | None = Query(None, ge=0)):
        try:
            # ANSWER m04 list_route BEGIN
            return select_products(store.all_products(), query=query,
                                   minimum_paise=minimum_paise, maximum_paise=maximum_paise)
            # ANSWER m04 list_route END
        except ValueError as error:
            raise HTTPException(422, str(error)) from error

    @app.get("/products/{product_id}", response_model=Product)
    def get_product(product_id: str):
        products = store.all_products()
        if product_id not in products:
            raise HTTPException(404, "Product not found")
        return products[product_id]

    @app.post("/orders", response_model=OrderResponse, status_code=201)
    def place_order(request: OrderRequest):
        try:
            # ANSWER m04 order_route BEGIN
            items = [(item.product_id, item.quantity) for item in request.items]
            order = build_order(items, store.all_products())
            store.save_order(order)
            return order.to_dict()
            # ANSWER m04 order_route END
        except KeyError as error:
            raise HTTPException(404, "Product not found") from error
        except ValueError as error:
            raise HTTPException(422, str(error)) from error

    @app.get("/orders/{order_id}", response_model=OrderResponse)
    def get_order(order_id: str):
        try:
            # ANSWER m04 retrieve_route BEGIN
            return store.get_order(order_id).to_dict()
            # ANSWER m04 retrieve_route END
        except KeyError as error:
            raise HTTPException(404, "Order not found") from error

    return app
