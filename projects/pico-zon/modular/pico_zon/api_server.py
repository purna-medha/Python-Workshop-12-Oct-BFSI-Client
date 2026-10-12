# Thin handlers translate HTTP requests into existing shopping operations.
# Startup initializes storage; importing the module does not create a database.
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from .api_schemas import OrderRequest, OrderResponse
from .cart import ShoppingCart
from .catalog import get_product, list_products
from .data_store import SQLiteStore
from .models import Product
from .shop import checkout


def create_app(store=None):
    if store is None:
        default_path = Path(__file__).resolve().parents[1] / "data/pico-zon.sqlite"
        store = SQLiteStore(os.getenv("PICOZON_DATABASE", str(default_path)))

    @asynccontextmanager
    async def lifespan(app):
        store.initialize()
        yield

    app = FastAPI(title="Modular Pico-Zon", lifespan=lifespan)

    @app.get("/products", response_model=list[Product])
    def products(query: str = ""):
        return list_products(query)

    @app.get("/products/{product_id}", response_model=Product)
    def product(product_id: str):
        try:
            return get_product(product_id)
        except KeyError as error:
            raise HTTPException(404, "Product not found") from error

    @app.post("/orders", response_model=OrderResponse, status_code=201)
    def place_order(request: OrderRequest):
        cart = ShoppingCart()
        try:
            for item in request.items:
                cart.add(item.product_id, item.quantity)
            return checkout(cart, store).to_dict()
        except KeyError as error:
            raise HTTPException(404, "Product not found") from error
        except ValueError as error:
            raise HTTPException(422, str(error)) from error

    @app.get("/orders/{order_id}", response_model=OrderResponse)
    def order(order_id: str):
        try:
            return store.get_order(order_id)
        except KeyError as error:
            raise HTTPException(404, "Order not found") from error

    return app


app = create_app()
