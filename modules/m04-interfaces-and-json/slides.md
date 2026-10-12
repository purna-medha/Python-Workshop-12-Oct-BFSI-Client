---
marp: true
theme: default
paginate: true
size: 16:9
title: "M4 · Connect independently running programs"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M4 · Connect independently running programs

Expose existing behavior through HTTP and interpret a response in a separate Python caller.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# Another process cannot reach your local variables

Communication needs an agreed representation and protocol.

```text
Python caller → HTTP request → route → domain operation
Python caller ← JSON response ← route ← result
```

The CLI and API can reuse the same rules while having separate process memory.

---

# Dependencies belong to a project environment

The standard library ships with Python; FastAPI and requests are third-party packages.

From `current-course/teaching-snippets/`:

```sh
uv sync --extra dev
uv run uvicorn m04.s03_order_api:app --port 8000
```

A second terminal runs the caller. Stop another server before reusing port 8000.

---

# A dictionary is a Python object; JSON is text

Serialization makes a value transferable beyond the current process.

```python
import json
payload = {"items": [{"product_id": "1", "quantity": 2}]}
text = json.dumps(payload)
restored = json.loads(text)
print(type(payload), type(text), restored == payload)
```

Encoding and decoding change representation, not the intended request.

---

# JSON has a smaller vocabulary than Python

JSON supports objects, arrays, strings, numbers, booleans, and null.

```python
import json
print(json.dumps({"available": True, "note": None}))
print(json.loads('{"available": true, "note": null}'))
```

A datetime needs an explicit representation. A tuple becomes an array; JSON object keys are strings.

---

# Dataclasses need translation before serialization

Convert a named record to ordinary structures before creating JSON text.

```python
from dataclasses import asdict
from m03.catalog import PRODUCTS
import json

product_data = asdict(PRODUCTS["1"])
print(json.dumps(product_data))
```

An arbitrary class instance is not automatically JSON-compatible.

---

# HTTP identifies an operation and its target

A request combines a method, a path, optional query values, and an optional body.

```text
GET  /products?q=cable      browse or search
GET  /products/1            retrieve one product
POST /orders               create an order using a body
GET  /orders/{order_id}     retrieve a saved order
```

The route is the public interface; the implementation remains behind it.

---

# Request locations carry different roles

A path identifies a resource; a query narrows selection; a body supplies structured data.

```json
{"items": [{"product_id": "1", "quantity": 2}]}
```

The caller supplies requested items. The server calculates prices and totals from its own catalog.

---

# Status codes describe the outcome of the request

A caller needs to know whether to interpret data or an error.

```text
200  resource returned
201  order created
404  requested resource not found
422  request cannot be accepted as supplied
500  server failed during processing
```

The response body supplies details; the status supplies the broad outcome.

---

# FastAPI registers a function as a route

The library decorator connects HTTP dispatch to a Python callable.

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/products")
def list_products():
    return [{"product_id": "1", "name": "USB-C Cable", "price_paise": 49900}]
```

This tiny example isolates registration. The working route delegates catalog selection.

---

# Path parameters become named arguments

A route can translate an external identifier into a domain lookup.

```python
from fastapi import HTTPException
from dataclasses import asdict
from m03.catalog import PRODUCTS

@app.get("/products/{product_id}")
def get_product(product_id: str):
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Unknown product")
    return asdict(PRODUCTS[product_id])
```

This extends the preceding `app`.

---

# Query parameters select rather than identify

A default makes an optional query choice explicit.

```python
@app.get("/products")
def list_products(q: str = ""):
    return [asdict(product) for product in PRODUCTS.values()
            if q.casefold() in product.name.casefold()]
```

Alternative list route using the earlier imports. Register one version when experimenting.

---

# A dataclass can describe the incoming body

Begin with the shape already understood in M3.

```python
from dataclasses import dataclass

@dataclass
class RequestedItem:
    product_id: str
    quantity: int

@dataclass
class OrderRequest:
    items: list[RequestedItem]
```

FastAPI uses Pydantic internally here. M5 makes application constraints explicit.

---

# A thin handler translates and delegates

The route does not need another copy of the checkout calculation.

```python
from m03.shop import create_order

@app.post("/orders", status_code=201)
def place_order(request: OrderRequest):
    items = [(item.product_id, item.quantity) for item in request.items]
    order = create_order(items)
    return {**asdict(order), "total_paise": order.total_paise}
```

Focused success-path excerpt; the complete M4 route also stores the order and maps failures.

---

# Translate domain failures at the HTTP boundary

Domain code expresses a shopping failure; a handler maps it into a protocol outcome.

```python
try:
    order = create_order(items)
except KeyError as error:
    raise HTTPException(status_code=404, detail="Unknown product") from error
except ValueError as error:
    raise HTTPException(status_code=422, detail=str(error)) from error
```

Handler-body excerpt. The domain operation remains usable without FastAPI.

---

# Generated documentation makes the interface explorable

Start the supplied M4 server, then open `http://127.0.0.1:8000/docs`.

Browse products, send the two-cable request, and retrieve its returned order ID.

The generated interface describes available operations. It does not prove their business behavior is correct.

---

# A caller must bound its wait

External I/O has a lifetime and can fail.

```python
import requests
response = requests.get("http://127.0.0.1:8000/products", timeout=5)
```

Requests timeouts bound connection/read waits, not a guaranteed five-second total workflow deadline.

---

# Check the status before treating the body as success

An HTTP response exists even when the operation was rejected.

```python
response.raise_for_status()
products = response.json()
print(products)
```

Continuation of the preceding request. `.json()` decodes text; M5 checks its application shape.

---

# Send structured data with the JSON argument

The requests library performs JSON encoding and supplies the content type.

```python
payload = {"items": [{"product_id": "1", "quantity": 2}]}
response = requests.post(
    "http://127.0.0.1:8000/orders", json=payload, timeout=5,
)
response.raise_for_status()
order = response.json()
```

The server returns its calculated total and generated ID.

---

# Predict what happens on an unknown product

Send the same request shape with product ID `999`.

Does the caller get no response, a response with an error status, or a created order?

At which line does `raise_for_status()` stop the normal success path?

---

# A rejection is a response rather than a transport failure

The supplied M4 API predicts **404** for the unknown product.

`raise_for_status()` raises `HTTPError`; the caller should not interpret the body as a created order.

A stopped server instead causes a connection failure: the caller could not complete the HTTP exchange.

---

# Failure categories guide useful recovery

Handle the specific case whose meaning you understand.

```python
try:
    response = requests.get("http://127.0.0.1:8000/products", timeout=5)
    response.raise_for_status()
except requests.HTTPError:
    print("Server rejected the request")
except requests.RequestException:
    print("Could not complete communication")
```

JSON decoding is a further boundary; catch it deliberately when decoding.

---

# A timeout does not establish whether an order was created

The server may finish a POST even if its response never reaches the caller.

```text
Caller sends order → server saves it → response is delayed
Caller times out   → actual server result is uncertain
```

Blindly repeating an order request can create a duplicate. Retry policy needs an explicit design.

---

# Process memory does not provide shared persistence

A module-level order dictionary survives only inside its process.

Restart the M4 server: earlier orders disappear. The separate CLI cannot see the API’s memory dictionary.

M6 introduces shared persistent records; serialization alone does not extend their lifetime.

---

# Codealong: trace the full exchange

Open [the notebook](codealong.ipynb), exploration 1. Start the M4 server separately.

Call browse, create, and retrieve. Annotate the Python object, JSON representation, HTTP status, and decoded object.

Keep returned IDs rather than inventing them.

---

# Codealong: inspect one failure at each boundary

In exploration 2, request an unknown product, then stop the server and repeat a GET.

Compare `HTTPError` with `ConnectionError`. Inspect a deliberate invalid JSON string separately.

Repair by choosing a known product, restarting the server, or correcting the serialized text.

---

# Expert review: locate duplicated rules

Review a handler that accepts `total_paise` from the caller and saves it unchanged.

Which domain promise could be bypassed? Remove that authority from the request and reuse the existing calculation.

Explain why route decorators and type hints do not replace domain rules.

---

# Transfer: define a public operation before its transport

Choose a shop feature and state its inputs, result, and rejected cases.

Then choose method, path, request representation, and status mapping.

Another language can implement the same protocol while using different internal records.

---

# Nano-Zon lab: apply the mechanism

Complete thin list/create/retrieve handlers and the JSON caller.

Start from the independent [M4 starter](../../projects/nano-zon/labs/m04/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m04/README.md) and [answer map](../../projects/nano-zon/labs/m04/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
uv run uvicorn nanozon.server:app --port 8000
```

**Expected:** A separate caller creates two cables with status 201 and total 99800; unknown product returns 404.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Expose a total-only endpoint by delegating to existing retrieval.

The [lab guide](../../projects/nano-zon/labs/m04/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Expose existing behavior through HTTP and interpret a response in a separate Python caller.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Validate boundaries and compose a workflow.
