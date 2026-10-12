# M8 — Establish collaboration and failure consequences

Integration tests run collaborating components for real. Controlled substitutes make external outcomes repeatable. A test's scope determines what it can establish, so choose each boundary deliberately.

**Start:** [starter/](starter/README.md). M7 tests are completed. Run `uv sync --extra dev`; no live server is needed. The store fixture uses a fresh temporary SQLite file and the client fixture builds an app around it.

## Complete five answer regions

Use [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. In `tests/test_integration.py`, check create/retrieve, the total, restart retrieval, and real stored line count.
2. Check that the supplied later-line failure leaves neither order headers nor lines.
3. In `tests/test_client.py`, check successful parsing, status checking, and the outgoing URL/payload/timeout.
4. Establish the client's timeout exception using a patched external call.
5. Assert distinct workflow outcomes for rejection, malformed JSON, and invalid response shape.

Fixtures, request setup, failure injection, and response mocks are written. The rollback fixture exposes HTTP 500 rather than re-raising server exceptions so the test can inspect both response and database state.

## Read the substitute before patching

In `tests/test_client.py`, `successful_response` supplies a response-shaped mock. `response.json.return_value` controls the value returned by `json()`; `side_effect` makes a method raise. Follow the chain from the patched `requests.post` to that response and then its decoded data. Only after that, inspect the patch target and the outgoing-call assertion.

## Observe completion

```sh
uv run --extra dev pytest tests/test_integration.py tests/test_client.py -q
```

The real API and SQLite establish round-trip persistence and rollback. Only the external HTTP boundary is replaced for client tests. Supplied checks also cover absent resources, preserved historical prices, duplicate stored IDs, source-data rejection without HTTP, and JSON report creation.

No regular application database is used, and no separate server process should be running for these checks. Passing mock interaction assertions alone would not establish that the real API persisted an order.

**Explain:** Which components run for real in each test, and which behavior is outside that test's scope?

**Expert review:** Why patch `nanozon.client.requests.post`? Explain why a transaction failure needs database assertions in addition to an exception or status check.

## Independent extension — no supplied answer

Add a workflow check for an external response whose JSON is a valid object but whose lines field is missing. Replace only requests.post; keep client validation real. Assert the invalid_response outcome and explain why this differs from a network timeout.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M9](../m09/README.md) investigates assertion quality and automates the checks.
