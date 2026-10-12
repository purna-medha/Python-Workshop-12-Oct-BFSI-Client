# M6 — Retain consistent information

Persistence gives data a longer lifetime than a process. Storage functions translate records, manage resources, and make related writes succeed or fail together.

**Start:** [starter/](starter/README.md). Earlier behavior works with memory storage. Read the supplied `nanozon/schema.sql` and `SQLiteStore.connect`; neither schema authoring nor connection plumbing is the learner task.

## Complete the storage operations

In `nanozon/storage.py`, follow [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. `all_products`: convert named rows into `Product` records.
2. `save_order`: write the header and all line snapshots within one transaction.
3. `get_order`: use a parameterized order-ID lookup for lines.
4. Finish reconstructing and checking the returned `Order`.

Initialization, seeds, foreign-key configuration, connection cleanup, absent-order detection, and caller wiring are supplied. The transaction context commits or rolls back; the outer connection context closes the resource.

## Enable and observe persistence

After completing the regions, launch:

```sh
NANOZON_STORAGE=sqlite python3 -m nanozon.cli
```

Add two cables and one bottle, then checkout. Copy the order ID, quit, relaunch the same command, and retrieve it with `order ORDER_ID`: the total is still ₹1,897.00.

For the persistent API, use `NANOZON_STORAGE=sqlite uv run uvicorn nanozon.server:app --port 8000`. The CLI and API share `data/nanozon.sqlite` when run from the same folder. `NANOZON_DATABASE` selects a different database file.

Inspect how `save_order` covers all writes. The controlled partial-save failure is provided as an executable integration exercise in M8; do not insert deliberate failures into the regular database. Changing today's product price must not rewrite saved order-line prices.

**Explain:** Why are catching an exception, rolling back changes, and closing a connection three different responsibilities?

**Expert review:** Explain duplicate submissions and duplicate stored IDs. Parameterized SQL binds values; it does not validate business rules for you.

## Independent extension — no supplied answer

Add SQLiteStore.order_count() with one SELECT COUNT(*) query. Compare the count before checkout, after checkout, and after reconnecting. Explain why retrieving the count should not create another order or change a saved total.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M7](../m07/README.md) supplies persistence completed and introduces test authoring.
