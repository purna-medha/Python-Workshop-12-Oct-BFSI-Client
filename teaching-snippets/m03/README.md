# M03 — Organize data, behavior, and responsibilities

Name records → own state → compose snapshots → separate modules.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_records.py](s01_records.py) | Give related data a named shape | `python -m m03.s01_records` |
| [s02_objects.py](s02_objects.py) | Give state an owner | `python -m m03.s02_objects` |
| [s03_composition_and_snapshots.py](s03_composition_and_snapshots.py) | Compose objects and preserve boundaries | `python -m m03.s03_composition_and_snapshots` |
| [s04_modules.py](s04_modules.py) | Divide a program by responsibility | `python -m m03.s04_modules` |

Run commands from the `current-course/teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

Snippet 04 uses small companion files: `catalog.py`, `records.py`, `shop.py`, `cart.py`, and `cli.py`. Each is at most 40 lines.

## Prediction and demonstration

**Before revealing the result:** Would replacing newly constructed OrderLine records with tuple(cart.items) preserve the original quantities?

**Teaching move:** Compare the reference diagram before and after snapshot construction. Explain what changing the cart can still affect. Use [s03_composition_and_snapshots.py](s03_composition_and_snapshots.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

No. A tuple prevents replacing its elements; it still references the mutable CartItem objects. New snapshot records preserve independent values.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m03/README.md) includes a small extension with no supplied answer.
