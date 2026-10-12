# M2 — Process collections and changing state

Collections organize many values, iteration applies rules repeatedly, and mutation changes an owned object. The shop now needs catalog selection and editable quantities in a local cart.

**Start:** [starter/](starter/README.md). M1 calculations are completed; run `python3 shop.py`.

## Complete collection operations

In `shop.py`, follow [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. `search_products`: filter by a case-insensitive name and optional price bounds. Preserve zero as a valid bound.
2. `add_item`: add units to the existing quantity rather than replacing it.
3. `update_item` and `remove_item`: change the supplied cart only after its supplied checks succeed.
4. `cart_subtotal`: iterate through the cart and reuse the M1 line-total function.

Only the selected operation bodies are disabled. Definitions, validation, the tiny catalog, and input handling remain written.

## Observe completion

Use `search CABLE` and `budget 0`; the first finds the cable and the second returns no products. Add two cables, add another cable, and inspect `cart`: the subtotal is ₹1,497.00. Update the cable quantity to one, add a bottle, and inspect ₹1,398.00. Remove the bottle, then checkout the cable.

Unknown IDs and non-positive quantities are rejected. An empty cart totals zero; empty checkout is rejected. A new `main` call creates a fresh dictionary rather than a shared default cart.

**Explain:** Which functions return selected data and which deliberately mutate their arguments?

**Expert review:** Would copying the catalog dictionary also copy its nested product records? Why does `maximum_paise is not None` matter?

## Independent extension — no supplied answer

Add product_ids_in_category(products, category) without changing the supplied records. Decide whether matching is case-sensitive and document it. Compare results for an existing category and one with no matches; explain your chosen collection type.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M3](../m03/README.md) introduces dataclass records and an object that owns this same shopping state.
