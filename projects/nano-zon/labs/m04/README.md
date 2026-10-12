# M4 — Connect a separate caller

An interface exposes operations through a protocol. Serialization lets independent programs exchange information; handlers translate requests into existing application behavior.

**Start:** [starter/](starter/README.md). The local shop is completed. From this folder run `uv sync`, then `uv run uvicorn nanozon.server:app --port 8000`. Use a second terminal for the caller and stop other servers on that port first.

## Complete the public operations

Follow [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. In `nanozon/api.py`, complete `list_products` by delegating to the supplied catalog query.
2. Complete `place_order`: translate dataclass items, build and save an order, and return its serializable data.
3. Complete `get_order` by retrieving the existing order and converting it for the response.
4. In `nanozon/client.py`, complete `submit_order` with a timeout, status checking, and JSON decoding.

Definitions, decorators, input dataclasses, error mapping, product lookup, and the server entry point are written. Both M4 and later capstone requests use an object containing `items`.

## Observe completion

Open `http://127.0.0.1:8000/docs`. List products, search for the cable, and request a missing product. Create an order with two cables: the response is 201 and the total is 99800 paise. Retrieve it by its returned ID.

Run `uv run python -m nanozon.call_api` in the second terminal. The caller browses, creates, and retrieves through HTTP rather than importing server state. Before completing a handler, the teaching API returns a deliberate 501 pending-lab response.

M4 callers use decoded dictionaries. From M5 onward the same client methods validate responses and return model objects, so callers use `order.total_paise` and `order.order_id`. The request shape remains unchanged.

The API's memory orders disappear when the server restarts. The CLI and API have independent memory stores; sharing persistent records comes in M6.

**Explain:** How do a Python dictionary, JSON text, and a received response differ?

**Expert review:** Which failures concern transport, HTTP rejection, or decoding? Why should the caller never choose the server's total?

## Independent extension — no supplied answer

Add GET /orders/{order_id}/total returning order_id and total_paise. Delegate to the existing store; use the same not-found response as order retrieval. Call it from a separate Python process and compare its total with the full order response.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M5](../m05/README.md) strengthens the boundary contract and automates a small workflow.
