# M1 — Express computations

Functions name reusable operations; values, expressions, and formatted strings express the result without requiring a framework. The shop needs readable product labels and correct price calculations.

**Start:** [starter/](starter/README.md). Run `python3 shop.py` from there. Collections and the command loop are supplied context that M2 will explain.

## Complete three small operations

In `shop.py`, use [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. `money`: separate rupees and remaining paise and return the formatted label.
2. `product_label`: combine an ID, name, and formatted price into one string.
3. `calculate_line_total`: return unit price multiplied by quantity. The supplied validation stays active.

Write or uncomment each answer and remove its `LAB-GUARD`. Return values; let the supplied CLI choose when to print them.

## Observe completion

Enter `list`, `add 1 2`, `add 3 1`, `cart`, `checkout`, then `cart`.

- Products display readable prices.
- The subtotal and receipt show ₹1,897.00.
- Successful checkout empties the cart.
- `add 1 0` is rejected by supplied validation.

Before completing the answers, relevant commands report a pending lab; help and quit remain available. `python3 tools/progress.py` should eventually report zero pending regions.

**Explain:** Why does returning a number let the application reuse a calculation more easily than printing it?

**Expert review:** Explain why storing integer paise and formatting rupees are separate responsibilities.

## Independent extension — no supplied answer

Add a discount_amount_paise(subtotal_paise, discount_percent) function. For this exercise, accept whole-number percentages from 0 to 100 and round down fractional paise with // 100. Check that 10% of 99800 is 9980 and 0% is zero. Keep it separate from checkout; explain its inputs and returned value.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M2](../m02/README.md) supplies these calculations completed and makes the collection operations the learner's responsibility.
