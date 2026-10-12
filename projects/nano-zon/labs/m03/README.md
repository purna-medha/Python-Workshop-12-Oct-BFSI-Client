# M3 — Give state an owner and preserve facts

Records name related data; objects own changing state; composition connects them. Checkout creates a historical boundary, so an order must retain independent quantities and prices.

**Start:** [starter/](starter/README.md). Run `python3 -m nanozon.cli`. This checkpoint guides the move from dictionaries to dataclasses; catalog queries and terminal wiring are supplied.

## Read the representation, then complete the behavior

Read `nanozon/models.py` first: `Product`, `CartItem`, `OrderLine`, and `Order` have written fields. Read the provided `ShoppingCart.__init__` to locate instance-owned state. Use [ANSWER-MAP.md](starter/ANSWER-MAP.md) for three answer regions:

1. `ShoppingCart.add`: construct the updated `CartItem` inside this instance.
2. `ShoppingCart.subtotal_paise`: combine line totals from owned items.
3. `build_order`: construct new immutable `OrderLine` snapshots from the requested values.

Remove guards as answers are enabled. Update, remove, checkout coordination, memory saving, and display are supplied so the lab focuses on ownership and composition.

## Observe completion

Add two cables, checkout, copy the order ID, then add five cables. Use `order ORDER_ID`: the original order still contains two units and totals ₹998.00. The new cart has five units. Create two `ShoppingCart` instances in the interpreter and explain why changing one does not change the other.

Orders exist only within this running process. Restart persistence arrives in M6.

**Explain:** Why does a tuple of mutable cart objects fail to establish an independent snapshot?

**Expert review:** Compare a computed total with storing another mutable total field. Identify which modules need no knowledge of terminal display.

## Independent extension — no supplied answer

Add a line_count property to Order that counts snapshot lines, rather than total units. An order with two cables on one line should report one line. Explain why this property needs no new mutable field.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M4](../m04/README.md) exposes these same operations through HTTP.
