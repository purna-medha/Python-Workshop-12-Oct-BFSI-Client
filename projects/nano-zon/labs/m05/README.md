# M5 — Validate boundaries and compose a workflow

Contracts establish acceptable structure; business rules depend on application facts. A workflow coordinates operations and records each outcome without confusing those two sources of rejection.

**Start:** [starter/](starter/README.md). M4 handlers and the client are complete. Run `uv sync` and start `uv run uvicorn nanozon.server:app --port 8000` in one terminal.

## Complete five focused regions

Use [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. In `nanozon/schemas.py`, enable a strict positive-integer quantity and a nonempty items constraint. Remove their temporary unconstrained field declarations marked `LAB-GUARD`.
2. In `nanozon/workflow.py`, complete `request_from_row`: CSV quantities arrive as strings and need explicit conversion.
3. Complete `process_row`'s submission and use the validated `OrderResponse` returned by the client. Failure categorization is already written.
4. Complete `run_workflow`'s JSON report write. File opening and iteration are supplied.

The five regions consist of two schema declarations and three function-body sections. Runtime validation comes from Pydantic rather than ordinary type hints.

## Required path and review extensions

The required learner work is the five answer regions: quantity and list constraints, CSV conversion, use of a validated response, and report writing. The client, loop, logging, environment lookup, and failure categories are supplied context. Trace one successful row and one rejected row before exploring the other outcomes.

After the required path, discuss coercion, omission versus null, extra fields, and configuration choices. Inspect `OrderRequest.model_json_schema()` as a brief preview of describing an interface to another program. Retries and a general-purpose API client are outside this lab.

The regular client now validates product and order responses before returning model objects. Successful HTTP and valid JSON alone do not establish the expected shape. Logging reports row/status progress; the saved JSON report retains all outcomes.

## Observe completion

In `/docs`, zero quantities and Boolean quantities are rejected by validation. A valid quantity for ID `999` reaches the domain and is rejected as an unknown product. Extra request fields are rejected rather than trusted as a supplied total.

Run `uv run python -m nanozon.workflow` from the second terminal. The supplied CSV should produce two created orders, two invalid-source rows, and one rejected unknown-product row. Inspect `data/order-report.json`; it retains source row numbers and distinct outcomes. Stop the server and explain how communication outcomes differ.

Each accepted CSV row creates an independent one-item order; the workflow does not group all rows into one purchase. Repeating the workflow creates additional orders.

**Explain:** At which step does text conversion fail, a constraint fail, and a valid-looking request fail a business rule?

**Expert review:** Discuss coercion, omission, null, and response validation. Identify one fact the schema cannot establish by itself.

## Independent extension — no supplied answer

Add a summarize_outcomes(outcomes) function returning counts by status. Derive the counts from outcomes rather than hard-coding the CSV expectations. Explain where it belongs in the workflow and why it should not submit another request.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M6](../m06/README.md) retains accepted orders after restart.
