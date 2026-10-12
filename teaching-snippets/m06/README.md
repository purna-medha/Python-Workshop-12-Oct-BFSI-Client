# M06 — Preserve information consistently

Manage resources → translate rows → retain facts → save atomically.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_persistent_resources.py](s01_persistent_resources.py) | Manage persistent resources | `python -m m06.s01_persistent_resources` |
| [s02_storage_records.py](s02_storage_records.py) | Translate storage representations | `python -m m06.s02_storage_records` |
| [s03_relationships.py](s03_relationships.py) | Preserve relationships and historical facts | `python -m m06.s03_relationships` |
| [s04_transactions.py](s04_transactions.py) | Treat related changes as one operation | `python -m m06.s04_transactions` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

The numbered demonstrations use disposable databases. `schema.sql` and the small storage companions supply the shared structure.

Optional persistent API: `uv run uvicorn m06.server:app --port 8000`. This creates `teaching-shop.sqlite`; `NANOZON_DATABASE` selects another path.

## Prediction and demonstration

**Before revealing the result:** If the second order line fails after the header and first line were inserted, how many new headers and lines should remain?

**Teaching move:** Inspect the two table counts after the supplied failure. Locate the transaction boundary that explains them. Use [s04_transactions.py](s04_transactions.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

Zero of each. All writes belong to one transaction; rollback removes the earlier writes when the later insertion fails.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m06/README.md) includes a small extension with no supplied answer.
