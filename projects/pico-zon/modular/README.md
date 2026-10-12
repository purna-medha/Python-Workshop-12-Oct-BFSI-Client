# Modular Pico-Zon

The same tiny shopping journey as the [50-line monolithic version](../pico_zon.py), organized into small modules. The terminal version has the same products, commands, repeated-unit receipt lines, integer-paise calculations, and cart-clearing behavior. Its core needs only the Python standard library.

This is the instructor's modular showcase. [Nano-Zon](../../nano-zon/README.md) supplies the richer learner labs, including quantity editing, CSV automation, normalized relational storage, and testing exercises.

## Run the terminal shop

From the training folder:

```sh
cd current-course/projects/pico-zon/modular
python3 -m pico_zon
```

Enter `1`, `1`, `3`, then `checkout`: the expected receipt total is ₹1,897.00. Enter `checkout` again to observe an empty cart. The commands remain product ID, `browse`, `checkout`, and `quit`.

Terminal orders are local snapshots; this menu displays receipts without saving them. The API layer adds SQLite saving and retrieval.

## Read by responsibility

| File | Responsibility | Teaching connection |
|---|---|---|
| [models.py](pico_zon/models.py) | Named product and immutable purchase records | Dataclasses and composition |
| [catalog.py](pico_zon/catalog.py) | Three products, lookup, and search | Collections and reusable functions |
| [cart.py](pico_zon/cart.py) | Each shopper's selection and subtotal | Instance-owned mutable state |
| [shop.py](pico_zon/shop.py) | Snapshot, optional save, then clear | Reusable business operations |
| [cli.py](pico_zon/cli.py) | Input, output, and readable rejections | Separation of presentation |
| [api_schemas.py](pico_zon/api_schemas.py) | Explicit request and response contracts | Runtime boundary validation |
| [api_server.py](pico_zon/api_server.py) | HTTP handlers calling existing operations | Publishing an interface |
| [data_store.py](pico_zon/data_store.py) | Save and retrieve orders with SQLite | Resource lifetime and persistence |
| [http_client.py](pico_zon/http_client.py) | Status checks, decoding, validated models | Calling a separate program |
| [web_app.py](pico_zon/web_app.py) | Browser products, cart, and retrieval | An HTTP-only user interface |

`__main__.py` starts the terminal interface; `__init__.py` identifies the package. Start with the first five files. Introduce the other layers only when their concepts are being taught.

## Run the API

From `modular/`:

```sh
uv sync --extra api
uv run --extra api uvicorn pico_zon.api_server:app --port 8000
```

Open `http://127.0.0.1:8000/docs`. Available operations:

| Method and path | Operation |
|---|---|
| `GET /products?query=cable` | Browse or search products |
| `GET /products/{product_id}` | Look up one product |
| `POST /orders` | Create and save a simulated order |
| `GET /orders/{order_id}` | Retrieve a saved order |

Submit this request to create two cables and one bottle:

```json
{"items": [{"product_id": "1", "quantity": 2}, {"product_id": "3", "quantity": 1}]}
```

The expected response is HTTP 201 with `total_paise` equal to 189700. Copy the returned order ID, restart the server, and retrieve it. Quantities must be positive integers; empty items fail validation, and unknown products receive 404. Prices are calculated from the server's catalog.

API startup creates `modular/data/pico-zon.sqlite`. `PICOZON_DATABASE` selects another file. Importing the API module does not initialize storage. SQLite stores one JSON snapshot per order in one committed insert; Nano-Zon demonstrates separate product, header, and line tables with multi-write transactions. Product data remains the fixed in-memory catalog.

Each API request builds its own temporary cart. The browser owns its selection until submission; no shared server cart is used. Repeated submissions create additional orders. No payment is taken.

## Run the browser interface

Keep the API running. In a second terminal, also from `modular/`:

```sh
uv sync --extra api --extra web
uv run --extra api --extra web python -m streamlit run pico_zon/web_app.py
```

Open the address Streamlit prints, normally `http://localhost:8501`. Add products, checkout, then copy the order ID into the Orders tab. `PICOZON_API_URL` selects the API address; its default is `http://127.0.0.1:8000`.

The web interface imports the HTTP client and communicates with the API. It has no direct access to the server's catalog or SQLite file. Client methods return validated models; `model_dump()` prepares a model for display.

## Teach the transition

1. **M1–M2:** Show the complete monolithic script and explain its values, functions, collections, and flow.
2. **M3:** Compare that script with the modular core. Locate the owner of cart state, the checkout rule, and the display functions. Predict why changing a cart cannot rewrite an order snapshot.
3. **M4–M5:** Trace browser → HTTP client → route → shopping operation → response. Distinguish valid shape from a product that actually exists.
4. **M6:** Inspect the saved snapshot and connection lifetime. Compare this single-document store with Nano-Zon's relational transaction exercise.
5. **M7–M9:** Use the existing snippets and Nano-Zon labs to learn test authoring, integration, coverage, and CI. This showcase adds no separate test curriculum.

AI extensions remain the separate Day 4 design.

**Authoring checks:** Syntax, TOML structure, and local links can be checked without dependencies. Terminal, API, database, and browser execution require runtime verification; no runtime test results are claimed here.
