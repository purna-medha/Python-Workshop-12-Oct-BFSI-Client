# Nano-Zon — completed reference

All essential application behavior and lab answer regions are active here. Use it to demonstrate the end state, inspect an answer, or compare a completed checkpoint.

## Reading order

| Area | Files |
|---|---|
| Values and calculations | `nanozon/calculations.py` |
| Catalog and records | `nanozon/catalog.py`, `nanozon/models.py` |
| State and snapshots | `nanozon/cart.py`, `nanozon/orders.py` |
| Interaction | `nanozon/cli.py` |
| Storage selection | `nanozon/runtime.py`, `nanozon/memory.py` |
| Public interface | `nanozon/api.py`, `nanozon/server.py`, `nanozon/client.py`, `nanozon/call_api.py` |
| Contracts and automation | `nanozon/schemas.py`, `nanozon/workflow.py`, `data/orders.csv` |
| Persistence | `nanozon/storage.py`, `nanozon/schema.sql` |
| Behavioral checks | `tests/` |
| Coverage and automation | `pyproject.toml`, `ci/nano-zon.yml` |

Run `python3 -m nanozon.cli` from this folder for the standard-library shopping application. For API/workflow commands, environment variables, and the lab structure, see the [capstone guide](../README.md).

Markers such as `# ANSWER m03 snapshot BEGIN` are navigation comments. They do not disable reference code. The starter builder uses them to comment only the selected current-module answer.

## Boundary and workflow conventions

Order requests use `{"items": [...]}`. The M5-and-later client validates product and order response shapes and returns Pydantic models; access an order with `order.total_paise` and `order.order_id`. The M4 starter deliberately returns decoded dictionaries before explicit client validation is introduced. Call signatures and `NANOZON_API_URL` stay consistent across teaching examples and labs.

The workflow configures logging in its CLI entry point and logs row numbers and statuses. Its saved JSON report remains the lasting record of outcomes. The HTTP client performs response validation once; workflow code uses the resulting model.
