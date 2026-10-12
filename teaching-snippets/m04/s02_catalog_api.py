# An interface exposes capabilities through an agreed protocol. HTTP assigns
# meaning to methods, paths, parameters, and status codes. A handler translates
# a request into existing application behavior rather than duplicating it.
#
# Publish catalog listing and lookup; FastAPI serializes the returned records.

from fastapi import FastAPI, HTTPException
from m03.catalog import PRODUCTS, Product

app = FastAPI(title="Teaching shop: catalog")


@app.get("/products")
def list_products(query: str = "") -> list[Product]:
    return [product for product in PRODUCTS.values()
            if query.casefold() in product.name.casefold()]


@app.get("/products/{product_id}")
def get_product(product_id: str) -> Product:
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    return PRODUCTS[product_id]


# From teaching-snippets: uv run uvicorn m04.s02_catalog_api:app --port 8000
# Open http://127.0.0.1:8000/docs; try /products?query=cable and /products/999.
# Route decorators register handlers. FastAPI already uses Pydantic internally.
