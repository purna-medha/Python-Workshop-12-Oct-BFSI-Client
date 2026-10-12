---
marp: true
theme: default
paginate: true
size: 16:9
title: "M3 · Give records a shape and state an owner"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M3 · Give records a shape and state an owner

Separate records, mutable behavior, historical snapshots, and presentation.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# A record names facts that belong together

Related facts need an explicit shape. A product has an identity, name, and price.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    price_paise: int
```

`@dataclass` is a supplied library decorator; it generates ordinary record conveniences.

---

# An instance supplies values for that shape

A class describes a kind of object. An instance holds one particular set of facts.

```python
cable = Product("1", "USB-C Cable", 49900)
bottle = Product("3", "Water Bottle", 89900)
print(cable.name, bottle.price_paise)
```

Attribute access names the fact instead of relying on a dictionary key spelling.

---

# Dataclasses generate routine record behavior

Generated initialization, representation, and equality keep the record definition focused on its fields.

```python
cable = Product("1", "USB-C Cable", 49900)
same_cable = Product("1", "USB-C Cable", 49900)
print(cable == same_cable)
print(cable is same_cable)
```

Equality compares field values here; identity asks whether this is the same object.

---

# Type annotations do not enforce domain rules

A field hint describes an intended type; dataclass construction does not validate it automatically.

```python
invalid_product = Product("1", "USB-C Cable", "expensive")
print(invalid_product.price_paise)
```

This deliberate example constructs successfully. M5 will introduce runtime boundary validation.

---

# Frozen records prevent attribute reassignment

A record can expose facts without allowing a caller to reassign its fields.

```python
cable = Product("1", "USB-C Cable", 49900)
# Deliberate failure if uncommented:
# cable.price_paise = 100
```

Expect `FrozenInstanceError`. Frozen is not a guarantee that nested mutable values become immutable.

---

# An object can own changes over time

Stateful behavior belongs near the state it manages.

```python
class ShoppingCart:
    def __init__(self):
        self.quantities = {}

    def add(self, product_id, quantity):
        self.quantities[product_id] = quantity
```

This tiny ownership example replaces a quantity; the complete shop validates and accumulates it.

---

# Self identifies the instance receiving a call

A method can operate on the particular cart used by the caller.

```python
first_cart = ShoppingCart()
second_cart = ShoppingCart()
first_cart.add("1", 2)
print(first_cart.quantities)
print(second_cart.quantities)
```

`__init__` runs for each new instance; `self` points to that instance.

---

# Predict what happens to shared class state

Will the second cart contain the cable?

```python
class SharedCart:
    quantities = {}

first = SharedCart()
second = SharedCart()
first.quantities["1"] = 2
print(second.quantities)
```

---

# Instance-owned state prevents accidental sharing

The predicted result is `{"1": 2}`: both instances reach the class dictionary.

```python
class ShoppingCart:
    def __init__(self):
        self.quantities = {}
```

Construct changing collections per instance; reserve class attributes for deliberately shared facts.

---

# Default factories create fresh mutable fields

A dataclass needs the same ownership decision as an ordinary class.

```python
from dataclasses import dataclass, field

@dataclass
class CartDraft:
    quantities: dict[str, int] = field(default_factory=dict)
```

The factory is called per instance. A shared mutable literal is not a suitable field default.

---

# Methods preserve rules around owned state

A useful method controls changes rather than merely exposing storage.

```python
class ShoppingCart:
    def __init__(self):
        self.quantities = {}

    def add(self, product_id, quantity=1):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.quantities[product_id] = self.quantities.get(product_id, 0) + quantity
```

Product lookup is supplied separately in the full implementation.

---

# Some operations remain ordinary functions

An operation with explicit inputs and no owned mutable state may need no class.

```python
def calculate_line_total(price_paise, quantity):
    return price_paise * quantity
```

A cart, an order, and a test can all reuse the same calculation. Organize by responsibility, not by making every noun a class.

---

# Composition connects useful parts

An order contains line records; each line retains the facts used at checkout.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    name: str
    unit_price_paise: int
    quantity: int
```

A cart’s current quantity and an order’s historical quantity have different lifetimes.

---

# A snapshot copies facts at a meaningful boundary

Create a new record when a changing draft becomes a completed order.

```python
quantity = 2
line = OrderLine("1", "USB-C Cable", 49900, quantity)
quantity = 5
print(line.quantity)
```

The snapshot still has two units. Copy every fact that history needs to retain.

---

# Predict whether a tuple alone makes a snapshot

What quantity does the order observe?

```python
cart_item = {"product_id": "1", "quantity": 2}
order_lines = (cart_item,)
cart_item["quantity"] = 5
print(order_lines[0]["quantity"])
```

---

# A fixed container can still hold changing objects

The predicted result is **5**. The tuple still references the same mutable dictionary.

Use new immutable line records containing scalar values. A tuple of those records gives the order stable contents for this model.

The snapshot guarantee comes from copying the relevant facts and choosing their representation.

---

# Derived values can stay connected to their source

A total calculated from lines cannot drift from a separately edited total field.

```python
@dataclass(frozen=True)
class Order:
    order_id: str
    lines: tuple[OrderLine, ...]

    @property
    def total_paise(self):
        return sum(line.unit_price_paise * line.quantity for line in self.lines)
```

`@property` exposes a calculation through attribute access.

---

# Checkout changes state only after success

A sequence must preserve the draft when order creation fails.

```python
def checkout(self):
    order = create_order(list(self.quantities.items()))
    self.quantities.clear()
    return order
```

Method excerpt from the teaching cart. `create_order` is supplied; M6 adds successful persistence before clearing the cart.

---

# Modules separate reasons for change

Records, rules, and display can evolve independently when dependencies stay deliberate.

```text
catalog.py   → product records and lookup
cart.py      → owned quantities
shop.py      → order construction
records.py   → historical order shapes
cli.py       → input and display
```

Follow these responsibilities in the modular Pico-Zon, not only the filenames.

---

# Import the operation rather than duplicate its rule

A caller depends on a public definition and supplies its inputs.

```python
from m03.cart import ShoppingCart

cart = ShoppingCart()
cart.add("1", 2)
order = cart.checkout()
print(order.total_paise)
```

Run from the teaching-snippets environment; the CLI owns display.

---

# An entry point distinguishes use from launching

Keep an interactive program from starting merely because another module imports it.

```python
def main():
    print("Pico-Zon entry point")

if __name__ == "__main__":
    main()
```

The guard runs `main` when launched as a script or module, not on ordinary import.

---

# Codealong: refactor one record without changing behavior

Open [the notebook](codealong.ipynb), exploration 1.

Replace a product dictionary with `Product`. Compare the name and price before and after.

Locate equivalent responsibilities in the [modular Pico-Zon](../../projects/pico-zon/modular/README.md).

---

# Codealong: change the cart after checkout

In exploration 2, add two cables, checkout, then add five cables.

Inspect both the new cart and the earlier order. Explain which object owns each quantity.

Find where the order’s total is computed, and where the CLI prints it.

---

# Expert review: review responsibility before adding abstraction

Consider a `PriceManager` class with no owned state and one multiplication method.

Would an ordinary function express the responsibility more clearly? Would a mutable total field create another fact to keep synchronized?

Optional inheritance review: a subclass can inherit behavior, but this shop needs composition rather than a product hierarchy.

---

# Recovery: inspect ownership when state leaks

If one cart sees another cart’s items, inspect class attributes and shared defaults first.

If an old order changes, inspect whether its lines contain references to mutable cart items.

Repair the representation, then repeat the same two-cart and post-checkout experiments.

---

# Transfer: draw the object boundary before writing syntax

Choose another shop feature: a wishlist, receipt, or promotion.

Which facts are records? Which state changes? Who owns it? Which facts must be historical?

Explain why the same responsibilities would exist in another programming language.

---

# Nano-Zon lab: apply the mechanism

Complete cart ownership, subtotal, and independent order snapshots.

Start from the independent [M3 starter](../../projects/nano-zon/labs/m03/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m03/README.md) and [answer map](../../projects/nano-zon/labs/m03/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
python3 -m nanozon.cli
```

**Expected:** After two-cable checkout, adding five cables does not change the earlier ₹998.00 order.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Add an order line_count property and distinguish lines from units.

The [lab guide](../../projects/nano-zon/labs/m03/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Separate records, mutable behavior, historical snapshots, and presentation.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Connect independently running programs.
