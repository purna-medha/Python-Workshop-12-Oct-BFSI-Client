---
marp: true
theme: default
paginate: true
size: 16:9
title: "M5 · Validate boundaries and compose a workflow"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M5 · Validate boundaries and compose a workflow

Accept explicit contracts, translate external text, and retain distinct workflow outcomes.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# Successful decoding does not establish usable data

A boundary needs several independent decisions.

```text
JSON syntax → expected shape and values → current business facts
```

A valid JSON object can omit items. A well-shaped item can name a nonexistent product.

---

# A model states the accepted structure

A contract names fields and constraints that external callers can depend on.

```python
from pydantic import BaseModel, ConfigDict, Field

class RequestedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: str = Field(min_length=1, strict=True)
    quantity: int = Field(strict=True, gt=0)
```

Positive quantity is checked before domain code receives the request.

---

# Collection constraints apply to the operation as a whole

A valid line is insufficient when the order contains no lines.

```python
class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[RequestedItem] = Field(min_length=1)
```

The public request remains `{"items": [...]}` from M4.

---

# Validation turns unknown data into a known interface

A model construction either supplies an accepted record or reports a validation failure.

```python
request = OrderRequest.model_validate({
    "items": [{"product_id": "1", "quantity": 2}],
})
print(request.items[0].quantity)
```

Model attributes become the caller’s interface after validation.

---

# Predict which inputs satisfy a strict quantity

Classify quantity values before running: `2`, `"2"`, `0`, `-1`, and `True`.

```python
RequestedItem(product_id="1", quantity=2)
```

Which require explicit conversion? Which must be rejected even though Python can use them in arithmetic?

---

# Strictness makes conversion a visible choice

Only integer **2** is accepted in that set. The string, zero, negative value, and Boolean fail.

A non-strict integer field may coerce numeric text. This course chooses strict quantity after explicit CSV conversion.

Type hints alone do not perform this validation; Pydantic construction does.

---

# Validation failures contain field locations

Inspect the structured explanation rather than replacing it with a generic success message.

```python
from pydantic import ValidationError
try:
    RequestedItem(product_id="1", quantity=0)
except ValidationError as error:
    print(error.errors()[0]["loc"])
    print(error.errors()[0]["type"])
```

The location connects the rejected input to the contract.

---

# Convert between model, dictionary, and JSON deliberately

A representation change should match the next boundary.

```python
request = OrderRequest.model_validate_json(
    '{"items":[{"product_id":"1","quantity":2}]}'
)
payload = request.model_dump()
print(payload)
```

Use `model_dump(mode="json")` when fields need JSON-compatible conversion.

---

# Extra fields require a stated policy

The contract must decide how to treat information it does not recognize.

```python
# Deliberately rejected by extra="forbid":
# RequestedItem(product_id="1", quantity=2, total_paise=1)
```

Rejecting an invented total avoids silently accepting a misspelled or unauthorized field.

---

# Domain rules use facts the schema does not possess

A nonempty ID and positive quantity do not establish catalog membership.

```python
from m03.shop import create_order
request = OrderRequest(items=[{"product_id": "999", "quantity": 1}])
items = [(item.product_id, item.quantity) for item in request.items]
# create_order(items) raises KeyError for the missing product.
```

Translate the domain rejection to HTTP 404 at the route.

---

# An adapter keeps the boundary separate from the domain

Use a short translation instead of making domain records depend on a web framework.

```python
def domain_items(request: OrderRequest):
    return [(item.product_id, item.quantity) for item in request.items]
```

Validation establishes structure; order construction establishes application behavior.

---

# Response contracts protect callers too

A status of 201 and parseable JSON do not guarantee the expected order shape.

```python
from m05.contracts import OrderResponse

order = OrderResponse.model_validate(response.json())
print(order.order_id, order.total_paise)
```

Continuation after status checking. The reusable client returns a model from M5 onward.

---

# Thin handlers can declare both directions

FastAPI connects explicit request and response contracts to existing operations.

```python
@app.post("/orders", response_model=OrderResponse, status_code=201)
def place_order(request: OrderRequest):
    return build_response(create_order(domain_items(request)))
```

Conceptual handler excerpt: `app` and `build_response` are supplied wiring. Response shape validation does not independently prove total arithmetic.

---

# CSV is a text boundary with named columns

Resource lifetime and text interpretation belong at the input boundary.

```python
import csv
from pathlib import Path

with Path("orders.csv").open(newline="", encoding="utf-8") as source:
    rows = list(csv.DictReader(source))
```

The values in each row are strings, including quantity.

---

# Convert external text before strict validation

Make the conversion decision observable and reusable.

```python
row = {"product_id": "1", "quantity": "2"}
request = OrderRequest(items=[{
    "product_id": row["product_id"],
    "quantity": int(row["quantity"]),
}])
```

`"two"` fails conversion; `"0"` converts but fails the positive quantity constraint.

---

# A workflow composes steps with distinct failures

Follow one row rather than building a general-purpose client.

```text
Read row → convert → validate → submit → validate response → retain outcome
```

Each accepted row creates one order. Repeating the workflow creates additional orders.

---

# Configuration varies independently of the operation

Choose the destination outside the workflow’s logic.

```python
import os
base_url = os.getenv("NANOZON_API_URL", "http://127.0.0.1:8000")
```

The default suits the classroom. The environment variable changes the destination without rewriting the submission function.

---

# A small client owns one external operation

Keep requests, status checking, and response validation in one place.

```python
import requests
from m05.contracts import OrderResponse

def submit_order(base_url, payload):
    response = requests.post(f"{base_url}/orders", json=payload, timeout=5)
    response.raise_for_status()
    return OrderResponse.model_validate(response.json())
```

The supplied production-of-the-lesson helper also trims a trailing URL slash.

---

# Retained outcomes make automation inspectable

An outcome answers what happened to one source row.

```python
outcome = {"row": 2, "status": "created", "order_id": order.order_id}
```

A failed row retains a different status and useful detail. The report preserves evidence after the process exits.

---

# Different failures need different outcome names

Trace each result to its boundary.

```text
invalid_source        conversion or source-contract failure
rejected              HTTP error response
communication_failed  transport or timeout failure
invalid_response      bad JSON or bad response shape
created               accepted, validated order response
```

A timeout leaves the server-side result uncertain; do not automatically repeat a POST.

---

# Catch a specific decoding error before its broader family

Requests JSON decoding errors are also request exceptions.

```python
try:
    order = submit_order(base_url, payload)
except requests.HTTPError:
    status = "rejected"
except requests.exceptions.JSONDecodeError:
    status = "invalid_response"
except requests.RequestException:
    status = "communication_failed"
except ValueError:
    status = "invalid_response"
```

Workflow excerpt; source validation happens before this block.

---

# Logs show progress; a report retains outcomes

Use each representation for its own audience and lifetime.

```python
import json, logging
from pathlib import Path
logger = logging.getLogger(__name__)
logger.info("Row %s: %s", outcome["row"], outcome["status"])
Path("order-report.json").write_text(
    json.dumps([outcome], indent=2), encoding="utf-8",
)
```

Console logging needs configuration; the saved report is still available later.

---

# Codealong: trace one accepted row and one rejected row

Open [the notebook](codealong.ipynb), exploration 1. Start the supplied M5 API.

Convert `"2"`, submit it, and inspect a validated `OrderResponse`. Try `"0"`, then a valid quantity for ID `999`.

Explain why only the last reaches the domain and receives HTTP rejection.

---

# Codealong: inspect the supplied workflow report

In exploration 2, explicitly enable the HTTP workflow after starting M5.

The sample CSV is expected to produce two created, two invalid-source, and one rejected row.

Compare source row numbers, statuses, and returned IDs. Stop the server and explain communication failure.

---

# Review extension: omission is different from null

A default can make a field optional to supply; allowing `None` is a separate choice.

```python
class OrderNote(BaseModel):
    note: str | None = None

missing = OrderNote()
explicit_null = OrderNote(note=None)
print(missing.model_fields_set, explicit_null.model_fields_set)
```

Both values are `None`; the supplied fields differ.

---

# Review extension: a schema describes an interface

A schema can help another program discover accepted structure.

```python
schema = OrderRequest.model_json_schema()
print(schema["properties"]["items"])
```

It describes fields and constraints, not current catalog membership. Day 4 can reuse this boundary description.

---

# Recovery: identify the boundary before fixing the data

A bad numeric string needs conversion repair. A zero quantity needs a changed request. An unknown ID needs a valid catalog choice.

A malformed successful response needs investigation of the server contract, not an invented total.

Keep the report entry even when processing other rows continues.

---

# Expert review: keep the required workflow narrow

Review the five required Nano-Zon regions: two constraints, CSV conversion, typed submission, and report writing.

Trace supplied plumbing; then consider coercion, omission, configuration, and schema inspection as extensions.

Do not add retries until duplicate-order behavior has an explicit policy.

---

# Nano-Zon lab: apply the mechanism

Enable quantity/list constraints, CSV conversion, typed submission, and report writing.

Start from the independent [M5 starter](../../projects/nano-zon/labs/m05/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m05/README.md) and [answer map](../../projects/nano-zon/labs/m05/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
uv run python -m nanozon.workflow
```

**Expected:** With the M5 API running: two created, two invalid-source, and one rejected source row.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Derive outcome counts from the report without making new requests.

The [lab guide](../../projects/nano-zon/labs/m05/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Accept explicit contracts, translate external text, and retain distinct workflow outcomes.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Retain information consistently.
