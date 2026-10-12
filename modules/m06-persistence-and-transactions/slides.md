---
marp: true
theme: default
paginate: true
size: 16:9
title: "M6 · Retain information consistently"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M6 · Retain information consistently

Save historical order facts, manage database resources, and make related writes atomic.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# Persistence gives facts a longer lifetime

A Python dictionary belongs to a process. A database file can outlive it.

```text
Create order → save file-backed records → exit process
Restart     → reconnect               → retrieve order
```

A stable database path identifies which history the application reopens.

---

# Storage representation serves a different purpose

Domain records express meaning; database tables organize retained facts.

```text
products     current identity, name, price
orders       order identity and checkout total
order_lines  order identity, position, product, snapshot facts
```

Nano-Zon uses related tables. Modular Pico-Zon uses one JSON snapshot per order row; today’s teaching examples expand it to related writes.

---

# SQLite access is part of the standard library

A connection opens a database resource.

```python
import sqlite3
connection = sqlite3.connect("shop.sqlite")
connection.close()
```

`:memory:` creates connection-local temporary state; a lasting file supports reopening.

---

# Resource cleanup and transaction outcome are separate

SQLite’s connection context commits or rolls back; it does not close the connection.

```python
from contextlib import closing
with closing(sqlite3.connect("shop.sqlite")) as connection:
    with connection:
        connection.execute("CREATE TABLE IF NOT EXISTS notes (text TEXT)")
```

The inner context handles the write outcome. The outer context closes the resource.

---

# Use temporary resources for deliberate experiments

A failure demonstration should affect only its own data.

```python
from tempfile import TemporaryDirectory
from pathlib import Path

with TemporaryDirectory() as directory:
    database_path = Path(directory) / "shop.sqlite"
    print(database_path)
```

The notebook’s database experiments use temporary files, not the regular Nano-Zon database.

---

# A schema states persistent structure

Keys identify records and constraints reject some invalid stored values.

```sql
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0)
);
```

The supplied schema supports application rules; it does not replace them.

---

# Bind values separately from SQL instructions

Parameters preserve the distinction between data and query structure.

```python
connection.execute(
    "INSERT INTO products VALUES (?, ?, ?)",
    ("1", "USB-C Cable", 49900),
)
```

Connection/body excerpt after schema setup. Do not interpolate external IDs into SQL text.

---

# A selection returns rows for explicit translation

Retrieve only the fields required by the next operation.

```python
row = connection.execute(
    "SELECT name, price_paise FROM products WHERE product_id = ?",
    ("1",),
).fetchone()
```

A one-element parameter tuple needs its comma. No matching row returns `None`.

---

# Missing data needs a deliberate outcome

Check absence before reading fields from the row.

```python
if row is None:
    raise KeyError("Unknown product")
```

The storage layer reports absence; the API later translates it into HTTP 404.

---

# Named rows make the translation readable

Set the row factory on each connection before fetching.

```python
connection.row_factory = sqlite3.Row
row = connection.execute(
    "SELECT product_id, name, price_paise FROM products WHERE product_id = ?",
    ("1",),
).fetchone()
```

Now fields can be read by name rather than position.

---

# Translate storage rows into domain records

The rest of the application should not need to understand SQL row mechanics.

```python
from m03.catalog import Product
product = Product(
    product_id=row["product_id"],
    name=row["name"],
    price_paise=row["price_paise"],
)
```

Continuation after the row is confirmed present.

---

# Updating current catalog data does not rewrite history

An update changes selected current records.

```python
with connection:
    connection.execute(
        "UPDATE products SET price_paise = ? WHERE product_id = ?",
        (99900, "1"),
    )
```

A saved order still uses its retained checkout-time unit price.

---

# Relationships connect facts without merging their lifetimes

An order line belongs to an order and identifies the product it refers to.

```sql
order_id TEXT NOT NULL REFERENCES orders(order_id),
product_id TEXT NOT NULL REFERENCES products(product_id)
```

Schema excerpt. Foreign keys connect identities; snapshot fields preserve historical name, price, and quantity.

---

# Enable foreign-key enforcement on every connection

SQLite requires an explicit connection setting for these relationships.

```python
connection.execute("PRAGMA foreign_keys = ON")
```

Do this before the transaction. The supplied connection helper applies it whenever a connection opens.

---

# Predict the price after a catalog update

An order saved two cables at 49900 paise each. The current cable price becomes 99900.

Which total should order retrieval return: 99800 or 199800?

Which fields need to be stored to make that result reproducible?

---

# A historical order uses its snapshot facts

The predicted total is **99800**. Save the line’s name, unit price, and quantity at checkout.

Joining an order to today’s product price cannot reconstruct that historical promise.

Keep the saved header total consistent with the sum of its saved line totals.

---

# A multi-write operation needs one success boundary

Saving a header and then failing a line must not leave a partial order.

```text
BEGIN → header → line 1 → line 2 → COMMIT
                         failure → ROLLBACK all related writes
```

Define the transaction around the complete logical operation.

---

# The transaction context covers the whole save

Keep all related writes within the same context.

```python
with connection:
    connection.execute(
        "INSERT INTO orders VALUES (?, ?)",
        (order.order_id, order.total_paise),
    )
    for line_number, line in enumerate(order.lines, start=1):
        save_line(connection, order.order_id, line_number, line)
```

`save_line` is an illustrative supplied insert helper; it must not commit separately.

---

# Catch after the transaction has rolled back

The exception must leave the transaction context so it can undo earlier writes.

```python
try:
    save_order(connection, order)
except sqlite3.IntegrityError as error:
    print("Order not saved:", error)
```

`save_order` owns the complete transaction. Catching inside and suppressing the failure can permit a partial commit.

---

# A deliberate later failure tests atomicity

The supplied temporary trigger rejects the bottle line after the cable line is attempted.

```python
header_count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
line_count = connection.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0]
print(header_count, line_count)
```

Expected in the fresh demonstration database: **0, 0** after rollback.

---

# Retrieval reconstructs a complete record

Storage lookup and domain reconstruction form the reverse translation.

```text
Find header → check absence → fetch lines in position order
            → construct immutable lines → construct order
            → compare computed total with saved total
```

An order’s line order should not depend on accidental database row order.

---

# A small dependency seam permits safe substitution

Give API code a connection provider rather than opening an unchangeable global file.

```python
from fastapi import Depends
from m06.api_dependencies import get_connection

@app.get("/products")
def list_products(connection=Depends(get_connection)):
    return load_products(connection)
```

Route excerpt; app and storage imports are supplied. M8 overrides the provider for isolated tests.

---

# Codealong: close and reopen the same temporary file

Open [the notebook](codealong.ipynb), exploration 1.

Save an order, close the connection, reopen the file, and retrieve it.

Change the catalog price and explain why the earlier order still totals 99800.

---

# Codealong: inspect both tables after a failed save

In exploration 2, run the supplied later-line failure in temporary storage.

Inspect the exception and both row counts. Explain the result if every write had committed separately.

Recovery is rollback and a valid next operation, not deleting rows from the regular shop database.

---

# Expert review: separate resource and failure responsibilities

Who chooses the database path? Who closes connections? Who decides transaction scope? Who maps failure to HTTP?

A duplicate stored ID can violate a primary key. Repeating a POST may generate a different ID and a second order.

These are different duplication problems; a primary key does not supply a retry policy.

---

# Transfer: identify the writes that belong together

For another shop feature, list the records that must change as one operation.

What inconsistency would appear if the second write failed? Place the transaction boundary around that promise.

The atomicity requirement remains meaningful with a different database or language.

---

# Nano-Zon lab: apply the mechanism

Translate rows, save complete orders atomically, and reconstruct historical records.

Start from the independent [M6 starter](../../projects/nano-zon/labs/m06/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m06/README.md) and [answer map](../../projects/nano-zon/labs/m06/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
NANOZON_STORAGE=sqlite python3 -m nanozon.cli
```

**Expected:** The saved ₹1,897.00 order can be retrieved after restart from the same database.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Add order_count using SELECT COUNT(*), then compare before and after reconnecting.

The [lab guide](../../projects/nano-zon/labs/m06/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Save historical order facts, manage database resources, and make related writes atomic.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Express behavioral promises as tests.
