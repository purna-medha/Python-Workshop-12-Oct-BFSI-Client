---
marp: true
theme: default
paginate: true
size: 16:9
title: "M2 · Process collections and manage changes"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M2 · Process collections and manage changes

Select many records, repeat operations, and make changes to state deliberately.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# One record becomes a collection of records

Collections represent multiplicity. Their shape should make the required operation clear.

```python
products = {
    "1": {"name": "USB-C Cable", "price_paise": 49900},
    "3": {"name": "Water Bottle", "price_paise": 89900},
}
cart = {"1": 2}
```

Here the cart maps an ID to its quantity; the opening Pico script used repeated IDs in a list.

---

# A list preserves order and allows repetition

Choose a list when position or repeated selections matter.

```python
product_ids = ["1", "1", "3"]
product_ids.append("1")
print(product_ids[0])
print(len(product_ids))
```

Indices begin at zero; an out-of-range index raises `IndexError`.

---

# A dictionary associates keys with values

Choose a dictionary when you look up a record by a stable identifier.

```python
prices = {"1": 49900, "3": 89900}
print(prices["1"])
print("999" in prices)
print(prices.get("999"))
```

Membership checks keys. A missing direct lookup raises `KeyError`.

---

# Tuple and set solve different representation needs

A tuple groups positions without allowing reassignment; a set keeps unique members.

```python
requested_item = ("1", 2)
product_id, quantity = requested_item
unique_ids = set(["1", "1", "3"])
print(len(unique_ids))  # 2
```

Do not rely on set iteration for display order.

---

# Nested structures still contain ordinary values

Follow each layer separately to find the fact needed by the calculation.

```python
product = {"name": "USB-C Cable", "price_paise": 49900}
products = {"1": product}
unit_price_paise = products["1"]["price_paise"]
```

A missing key at either level is a different failed assumption.

---

# Iteration repeats a rule over known members

A loop gives each member a turn without duplicating the operation.

```python
prices = {"1": 49900, "3": 89900}
for product_id, price_paise in prices.items():
    print(product_id, price_paise)
```

Use `.items()` when both the key and its associated value matter.

---

# Accumulation combines many contributions

Initialize the result once, then add each line’s contribution.

```python
prices = {"1": 49900, "3": 89900}
cart = {"1": 2, "3": 1}
subtotal_paise = 0
for product_id, quantity in cart.items():
    subtotal_paise += prices[product_id] * quantity
print(subtotal_paise)
```

---

# Predict the empty collection result

What is returned when no iterations run?

```python
def subtotal(cart, prices):
    result = 0
    for product_id, quantity in cart.items():
        result += prices[product_id] * quantity
    return result

print(subtotal({}, {"1": 49900}))
```

---

# The initial value defines the empty result

The predicted result is **0**. An empty cart contributes no lines.

Checkout may still reject an empty cart: totaling data and allowing an operation are different responsibilities.

Choose the initial accumulator to match the operation, rather than adding a special empty-cart arithmetic path.

---

# Filtering expresses which members belong

Write the selection rule clearly before compressing its syntax.

```python
names = ["USB-C Cable", "Water Bottle"]
matches = []
for name in names:
    if "cable" in name.casefold():
        matches.append(name)
```

The result is a new list; the original catalog names remain unchanged.

---

# A comprehension names a simple transformation

When the loop has one clear selection and result, a comprehension can retain its meaning.

```python
names = ["USB-C Cable", "Water Bottle"]
matches = [name for name in names if "cable" in name.casefold()]
```

Prefer the earlier loop when additional branching or side effects obscure the idea.

---

# Sorting derives an order without rewriting the source

Presentation order can be an output of a calculation.

```python
products = [
    {"name": "Cable", "price_paise": 49900},
    {"name": "Bottle", "price_paise": 89900},
]
cheapest_first = sorted(products, key=lambda item: item["price_paise"])
```

The small anonymous function supplies one sorting key.

---

# Grouping collects related records under one key

Accumulation can produce a collection rather than a number.

```python
selected_ids = ["1", "1", "3"]
quantities = {}
for product_id in selected_ids:
    quantities[product_id] = quantities.get(product_id, 0) + 1
print(quantities)
```

Repeated selections become quantities: `{"1": 2, "3": 1}`.

---

# Counted iteration and positions have explicit tools

Use `range` for a count and `enumerate` for a position plus value.

```python
for attempt in range(2):
    print("Attempt", attempt + 1)
for position, product_id in enumerate(["1", "3"], start=1):
    print(position, product_id)
```

The upper bound of `range` is excluded.

---

# A while loop repeats until state changes

An interactive command loop has no predetermined number of commands.

```python
commands = iter(["browse", "quit"])
while True:
    command = next(commands)
    if command == "quit":
        break
    print(command)
```

`break` ends the loop; the supplied Pico CLI reads commands from `input` instead.

---

# Continue skips the rest of one iteration

Keep a loop readable when one input should be ignored.

```python
for command in ["", "browse", "quit"]:
    if not command:
        continue
    if command == "quit":
        break
    print(command)
```

An empty string is false in a condition; a nonempty string is true.

---

# A valid zero is different from an absent value

Truthiness is convenient only when every false value has the same meaning.

```python
maximum_paise = 0
if maximum_paise is not None:
    print("Apply the zero-price filter")
```

`None` means no bound. Zero means accept only products within a zero bound.

---

# Defaults and keyword arguments clarify a caller’s choice

A function interface states which inputs can be omitted and what omission means.

```python
def within_budget(price_paise, *, maximum_paise=None):
    """Return whether a price satisfies the optional upper bound."""
    return maximum_paise is None or price_paise <= maximum_paise

print(within_budget(49900, maximum_paise=0))
```

`*` makes the following parameter keyword-only.

---

# Type hints document the intended interface

Hints help readers and tools; a hint alone does not reject a wrong value.

```python
def line_total(price_paise: int, quantity: int = 1) -> int:
    return price_paise * quantity

print(line_total(49900, quantity=2))
```

Defaults belong in the definition; keyword arguments belong in the call.

---

# Aliases expose one mutable object through two names

Assignment of a collection shares a reference; it does not duplicate the collection.

```python
cart = ["1"]
other_name = cart
other_name.append("3")
print(cart)
```

Both names now observe `["1", "3"]`.

---

# A shallow copy duplicates only the outer container

Copy depth must match the state whose ownership matters.

```python
cart = [{"product_id": "1", "quantity": 2}]
copied_cart = cart.copy()
copied_cart[0]["quantity"] = 5
print(cart[0]["quantity"])
```

The inner dictionary is still shared. M3 creates new records for historical snapshots.

---

# Predict the mutable default trap

What does the second call return?

```python
def remember(product_id, cart=[]):
    cart.append(product_id)
    return cart

remember("1")
print(remember("3"))
```

---

# A default is created when the definition runs

The predicted result is `["1", "3"]`: both calls use the same default list.

```python
def remember(product_id, cart=None):
    if cart is None:
        cart = []
    cart.append(product_id)
    return cart
```

Now omitted carts are fresh; explicitly supplied carts still change deliberately.

---

# Reject bad values before changing state

An operation should preserve state when its prerequisites fail.

```python
def add(cart, product_id, quantity):
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")
    cart[product_id] = cart.get(product_id, 0) + quantity
```

`True` is an integer subclass; the exact type check rejects it here.

---

# Handle expected failures at the interaction boundary

Convert an expected input failure into useful feedback; allow unrelated defects to surface.

```python
quantity_text = "two"
try:
    quantity = int(quantity_text)
except ValueError:
    print("Enter a whole-number quantity")
```

Do not catch every exception to make the CLI appear successful.

---

# Imports let another module reuse the same operation

A module groups definitions under a name.

```python
from m03.shop import calculate_line_total
print(calculate_line_total(49900, 2))
```

This is a preview of the supplied helper. M3 will organize records, state, and display into modules.

---

# Codealong: choose the right collection and trace a loop

Open [the notebook](codealong.ipynb), exploration 1.

Turn `["1", "1", "3"]` into a quantity dictionary, then calculate 189700 paise.

Try an empty list. Explain why the result contains no quantities and totals zero.

---

# Codealong: investigate who sees a change

In exploration 2, compare an alias, a shallow copy, and a fresh cart.

Change one nested quantity and predict every observed value. Then replace a truthiness-based price filter with an explicit `None` check.

Optional: recognize `*args` as a tuple of extra positional arguments and `**kwargs` as a dictionary of extra keyword arguments.

---

# Nano-Zon lab: apply the mechanism

Search and filter products; add, update, remove quantities; calculate subtotal.

Start from the independent [M2 starter](../../projects/nano-zon/labs/m02/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m02/README.md) and [answer map](../../projects/nano-zon/labs/m02/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
python3 shop.py
```

**Expected:** Case-insensitive search works; zero is a real price bound; independent carts stay separate.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Select product IDs by category and justify the result collection.

The [lab guide](../../projects/nano-zon/labs/m02/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Select many records, repeat operations, and make changes to state deliberately.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Give records a shape and state an owner.
