# Nano-Zon — the M1–M9 capstone

A small complete shopping application, built from the same general programming concepts as the [teaching snippets](../../teaching-snippets/README.md) and [dense chapters](../../teaching-text/README.md). Each lab extends a capability while supplied plumbing keeps the task focused.

## What is here

| Folder | Role |
|---|---|
| [reference/](reference/README.md) | Complete working application with active answer regions |
| [day-one/shop.py](day-one/shop.py) | Completed procedural representation for M1/M2, before classes or frameworks |
| [labs/](labs/README.md) | Nine lab guides, each with its own ready-to-edit starter checkpoint |
| [tools/build_starters.py](tools/build_starters.py) | Recreate a lab in a new folder without overwriting participant work |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | Build decisions and implementation record |

The reference is named `reference` because this repository ignores folders named `solution`.

## Participant answer convention

The starter contains written definitions, parameters, records, validation scaffolding, and application wiring. Only the current module's answer regions are commented out. Earlier answers are active. For example:

```python
def calculate_line_total(unit_price_paise, quantity):
    validate_quantity(quantity)          # Supplied context remains active.
    # ANSWER m01 line_total BEGIN
    # return unit_price_paise * quantity
    raise NotImplementedError("M01: complete line_total")  # LAB-GUARD: remove when answering
    # ANSWER m01 line_total END
```

Write or uncomment the answer, then remove its `LAB-GUARD` line. Preserve indentation. Answers are intentionally visible for guided completion; this is a learning scaffold rather than a closed-book assessment. A function guard reports unfinished behavior instead of silently returning an incorrect value. M5 field declarations use temporary unconstrained fields; remove those guard declarations when enabling their constrained replacements. M9 configuration answers are commented configuration rather than Python guards.

Every starter has an `ANSWER-MAP.md` with exact locations. `python tools/progress.py` lists pending regions without importing the application. It establishes completion of the scaffolding, not correctness of an answer.

## Essential capabilities

- Browse, look up, search, and filter the three familiar products.
- Add repeated quantities, update or remove cart items, and calculate integer-paise totals.
- Reject invalid quantities, unknown products, and empty checkout.
- Create immutable simulated purchase snapshots and clear a cart only after successful saving.
- Publish product and order APIs; make calls from a separate Python client.
- Validate request/response contracts, return validated client models from M5 onward, and produce a CSV-driven JSON outcome report with progress logging.
- Store products, orders, and order lines in SQLite; retrieve orders after restart.
- Save headers and lines in one transaction so partial failures leave no partial order.
- Supply domain, schema, integration, client, and test-quality exercises, coverage configuration, and a CI template.

Products match Pico-Zon: USB-C Cable ₹499, Mechanical Keyboard ₹5,499, Steel Water Bottle ₹899. IDs are strings and stored prices are integer paise. There are no real payments, accounts, shipping, inventory reservations, or AI features.

## Start with a lab

```sh
cd projects/nano-zon/labs/m01/starter
python3 shop.py
python3 tools/progress.py
```

Read the parent [M1 guide](labs/m01/README.md) and complete the three selected functions. Pending features report the lab location. The command shell still starts before those answers are enabled.

Each parent lab guide also includes an independent extension with no supplied answer. These complement guided completion and let learners explain a design choice or demonstrate a new behavior. The next module supplies a checkpoint with the preceding core module completed. Keep your completed folders for comparison. M3 is a guided change from dictionaries to dataclasses and objects; API and database capabilities arrive only when their modules begin.

## Run the complete application

```sh
cd projects/nano-zon/reference
python3 -m nanozon.cli
```

Use `list`, `search cable`, `budget 100000`, `add 1 2`, `add 3 1`, `cart`, and `checkout`. The total is ₹1,897.00. Copy the displayed order ID, restart, and use `order ORDER_ID` to retrieve it. Use `help` for the complete command list.

The finished reference defaults to SQLite at `data/nanozon.sqlite`. `NANOZON_DATABASE` selects another path. `NANOZON_STORAGE=memory` chooses process-local storage. M3–M6 starters default to memory so incomplete SQL does not disable earlier shopping behavior; M6 explicitly enables SQLite after its answers are complete.

For APIs and workflows:

```sh
uv sync --extra dev
# Terminal 1, from reference/:
uv run uvicorn nanozon.server:app --port 8000
# Terminal 2, also from reference/:
uv run python -m nanozon.call_api
uv run python -m nanozon.workflow
```

API documentation is at `http://127.0.0.1:8000/docs`. `NANOZON_API_URL` configures callers. M4 and later capstone requests use `{"items": [...]}` consistently; M5 strengthens validation without changing that shape. CLI and API share the SQLite file in the reference, but each process has separate orders when using memory storage.

The CSV creates two independent orders, rejects the unknown product, and records two invalid-source rows. Every repeated submission creates a new order with a server-generated UUID; automatic retry and idempotency are not implemented. An attempted duplicate stored order ID is rejected.

## Testing and CI labs

M7–M9 supply real test functions and fixtures as teaching material. From a completed project:

```sh
uv run --extra dev pytest -q
uv run --extra dev pytest --cov=nanozon --cov-branch --cov-report=term-missing
```

Tests use temporary databases and controlled external HTTP, so they need no live server. The [CI template](reference/ci/nano-zon.yml) remains inactive until copied into a repository's `.github/workflows/` directory. For a nested project, set its run-step working directory and report path appropriately.

**Authoring verification:** Python syntax and generated answer boundaries are inspected during creation; ordinary CLI/SQLite demonstrations are used to inspect the shopping flow. Framework execution and pytest verification are separate pending steps until dependencies are installed and the suite is explicitly run.
