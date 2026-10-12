---
marp: true
theme: default
paginate: true
size: 16:9
title: "M8 · Establish component collaboration"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M8 · Establish component collaboration

Run local components together and control the external outcomes a client must handle.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# A correct component can still disagree with its neighbor

Integration checks the handoff between real implementations.

```text
Request JSON → validation → domain order → SQL writes → response JSON
```

Unit tests of multiplication do not establish that a route saves its calculated order.

---

# The test boundary determines the claim

Choose which components participate before choosing tools.

```text
Unit         one behavior with controlled surrounding inputs
Integration  real local components across a boundary
Workflow     coordinated steps and retained outcomes
```

State what remains outside the check: browser, live network, or deployed infrastructure.

---

# TestClient exercises routes without a separate server

The application handles real request decoding, validation, and domain calls in process.

```python
from fastapi.testclient import TestClient
from m05.s03_validation_and_rules import app

with TestClient(app) as client:
    response = client.post("/orders", json={
        "items": [{"product_id": "1", "quantity": 2}],
    })
```

This M5 example checks an in-memory route, not SQLite persistence.

---

# Assert the response’s behavioral content

A status code and a total establish different facts.

```python
assert response.status_code == 201
assert response.json()["total_paise"] == 99800
assert response.json()["lines"][0]["name"] == "USB-C Cable"
```

Continuation of the preceding exchange. Calling the route alone establishes no comparison.

---

# Validation and business rejection need separate cases

Exercise the same request shape with different rejected facts.

```python
invalid = client.post("/orders", json={
    "items": [{"product_id": "1", "quantity": 0}],
})
missing = client.post("/orders", json={
    "items": [{"product_id": "999", "quantity": 1}],
})
```

Within an active client context: expect 422 for invalid quantity and 404 for unknown product.

---

# A fresh file isolates database side effects

Give each test a database that no other test or regular application owns.

```python
import pytest

@pytest.fixture
def database_path(tmp_path):
    return tmp_path / "shop.sqlite"
```

Initialize the supplied schema and seed products before using it. `tmp_path` provides a new temporary folder per test.

---

# A dependency override redirects one resource seam

Keep the real route and storage logic; replace where its connection comes from.

```python
from m06.database import connect
from m06.api_dependencies import get_connection

def test_connection():
    with connect(database_path) as connection:
        yield connection

app.dependency_overrides[get_connection] = test_connection
```

Fixture-body excerpt. Open the connection inside the request execution; clear the override during cleanup.

---

# Fixture lifetime includes cleanup after use

A yielded fixture can keep a client open for the test and close it afterward.

```python
@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

Illustrative fixture using a supplied app fixture; see the actual setup in `m08/conftest.py`.

---

# A round trip follows the returned identity

Create and retrieve the same order rather than assuming a generated ID.

```python
created = client.post("/orders", json=payload)
assert created.status_code == 201
order = created.json()
retrieved = client.get(f"/orders/{order['order_id']}")
assert retrieved.status_code == 200
assert retrieved.json() == order
```

Inside a test with the isolated client and known two-cable payload.

---

# Inspect storage when the promise includes persistence

A response could be correct even if nothing was saved.

```python
with connect(database_path) as connection:
    count = connection.execute(
        "SELECT COUNT(*) FROM order_lines WHERE order_id = ?",
        (order["order_id"],),
    ).fetchone()[0]
assert count == 1
```

One line holds two units. This is a continuation of the one-product round trip.

---

# Reopening proves more than reading live memory

To establish persistence, reopen the store with the same temporary database path.

```text
Client A creates → close its context → new app/store instance
                → retrieve same order → compare historical facts
```

Nano-Zon’s lab checks restart retrieval explicitly. A route round trip in one process alone does not establish that.

---

# Predict what a failure response leaves behind

A supplied SQL trigger rejects the second line after the first line is attempted.

If the API returns 500, what should the two database counts be?

Does a status assertion alone establish that rollback occurred?

---

# Rollback needs evidence about the resulting state

Expected after the controlled failure: **zero headers and zero lines** in the fresh database.

```python
assert failed.status_code == 500
assert header_count == 0
assert line_count == 0
```

The fixture supplies the failure setup and counts. An exception alone could coexist with partial writes.

---

# Expose the response when investigating server failures

TestClient normally raises server exceptions into the test.

```python
with TestClient(app, raise_server_exceptions=False) as client:
    failed = client.post("/orders", json=payload)
```

For the rollback lesson this permits checking HTTP 500, then inspecting the database. It does not suppress the stored-state assertions.

---

# Controlled failure belongs in the temporary fixture

Use the supplied later-line trigger only in isolated test storage.

Keep SQL trigger plumbing supplied; explain that it fails after earlier writes have occurred.

A failure before any insert would not exercise rollback of a partial save.

---

# External HTTP outcomes need controlled substitutes

The automation client can be tested without a live server by replacing its external call.

```text
Real client parsing and validation ← controlled response object
```

Keep local behavior real. A mocked API response does not prove the real API saved an order.

---

# A response-shaped mock provides a known interface

Specify the object whose behavior the client expects.

```python
import requests
from unittest.mock import Mock
response = Mock(spec=requests.Response)
response.raise_for_status.return_value = None
response.json.return_value = {
    "order_id": "example-order", "total_paise": 99800,
    "lines": [{"product_id": "1", "name": "USB-C Cable",
               "unit_price_paise": 49900, "quantity": 2}],
}
```

A specification catches unknown attributes; it does not prove semantic realism.

---

# Return values control successful calls

A mock returns configured data when the client invokes the expected method.

```python
print(response.json()["total_paise"])
response.raise_for_status()
```

The response model still validates this dictionary in the real client. The mock is not a replacement for that model.

---

# Side effects provide deliberate exceptions

A failure can be configured at the external operation that produces it.

```python
response.raise_for_status.side_effect = requests.HTTPError("404")
```

Calling this method now raises. Use `side_effect` on `json` for malformed data, or on `post` for a timeout.

---

# Patch the name used by the code under test

Replace the external callable where the client looks it up.

```python
from unittest.mock import patch
from m05.http_client import submit_order

with patch("m05.http_client.requests.post", return_value=response):
    order = submit_order("http://shop.test", payload)
```

The context restores the patched name afterward. Reset the response to its success behavior for this example.

---

# Check both parsing and the outgoing request

A correctly parsed result can accompany an incorrectly formed request.

```python
with patch("m05.http_client.requests.post", return_value=response) as post:
    order = submit_order("http://shop.test", payload)
assert order.total_paise == 99800
post.assert_called_once_with(
    "http://shop.test/orders", json=payload, timeout=5,
)
```

This establishes the client’s contract with the substitute, not actual network delivery.

---

# A timeout should retain its meaning

The client should not turn communication failure into a created order.

```python
with patch("m05.http_client.requests.post", side_effect=requests.Timeout("slow")):
    with pytest.raises(requests.Timeout):
        submit_order("http://shop.test", payload)
```

The workflow maps that failure to `communication_failed`; the server-side outcome remains uncertain.

---

# Parseable JSON can still violate the response contract

A missing line field is different from a network timeout.

```python
response.json.return_value = {"order_id": "example-order", "total_paise": 99800}
```

Real Pydantic validation rejects this response. The workflow should retain `invalid_response`, not invent missing lines.

---

# Codealong: run local components together

Open [the notebook](codealong.ipynb), exploration 1.

Use a temporary SQLite file, the supplied connection override, and the real API.

Create and retrieve two cables, inspect the stored line count, and explain which components ran for real.

---

# Codealong: replace only the external call

In exploration 2, supply a successful response, then a timeout, then missing response fields.

Keep client validation real. Explain each outcome and the limits of the mock’s evidence.

Do not need a separately running server for either exploration.

---

# Expert review: detect a test that proves its own mock

If both the route and store are replaced, can the test establish persistence?

Choose real local components for that claim. Replace the external HTTP boundary only when investigating client decisions.

Review cleanup so one test cannot leave an override that changes the next test.

---

# Recovery: trace a failure to its boundary

Wrong total: inspect domain behavior. Correct response but no rows: inspect storage wiring.

Regular database changed: repair fixture isolation. Mock not used: inspect the imported name at its lookup location.

Repeat the smallest relevant test after the repair, then the broader suite.

---

# Nano-Zon lab: apply the mechanism

Assert real persistence and rollback; check controlled client and workflow failures.

Start from the independent [M8 starter](../../projects/nano-zon/labs/m08/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m08/README.md) and [answer map](../../projects/nano-zon/labs/m08/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
uv run --extra dev pytest tests/test_integration.py tests/test_client.py -q
```

**Expected:** Real API/SQLite checks use fresh storage; external HTTP substitutes expose distinct failures.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Return valid JSON with a missing lines field and establish invalid_response.

The [lab guide](../../projects/nano-zon/labs/m08/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Run local components together and control the external outcomes a client must handle.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Maintain useful evidence as software changes.
