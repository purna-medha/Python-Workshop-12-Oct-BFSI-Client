---
marp: true
theme: default
paginate: true
size: 16:9
title: "M1 · Express behavior with values and functions"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M1 · Express behavior with values and functions

Trace inputs into results, choose behavior, and name a reusable calculation.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# A working application gives the pieces a purpose

Run the supplied 50-line Pico-Zon: browse, add cable twice, add bottle, checkout.

```sh
python3 projects/pico-zon/pico_zon.py
```

Predict the receipt: ₹1,897.00. Lists and loops are a preview; today we explain values and functions.

---

# Names connect a problem to its representation

A program acts on representations of facts. Choose names that expose their meaning.

```python
product_id = "1"
product_name = "USB-C Cable"
unit_price_paise = 49900
quantity = 2
```

The ID identifies; the price measures; the quantity counts.

---

# Types determine which operations make sense

A type gives a value its available operations. Python values carry their types at runtime.

```python
print(type("1"))      # str
print(type(49900))    # int
print(type(1.5))      # float
print(type(True))     # bool
print(type(None))     # NoneType
```

A missing value and a numeric zero express different facts.

---

# Text at an input boundary needs interpretation

Input arrives as text. Conversion decides whether that text can become a quantity.

```python
quantity_text = "2"
quantity = int(quantity_text)
print(quantity * 49900)
```

Conversion can fail: a text label is not automatically a number.

---

# Expressions combine facts into new values

An expression evaluates to a value that the rest of the application can use.

```python
unit_price_paise = 49900
quantity = 2
line_total_paise = unit_price_paise * quantity
print(line_total_paise)
```

The unit price stays unchanged; the result represents two units.

---

# Predict how assignment changes a name

Read before running. Which amount is printed?

```python
quantity = 2
line_total_paise = 49900 * quantity
quantity = 3
print(line_total_paise)
```

Does changing an input automatically recompute a previous result?

---

# Assignment stores the result of that evaluation

The predicted result is **99800**. The earlier expression evaluated when its line ran.

```python
quantity = 3
line_total_paise = 49900 * quantity
print(line_total_paise)  # 149700
```

Recompute explicitly when the inputs change.

---

# Integer minor units keep money arithmetic explicit

Represent stored money as integer paise; render rupees only at the display boundary.

```python
amount_paise = 49905
rupees = amount_paise // 100
remaining_paise = amount_paise % 100
```

`//` gives whole rupees; `%` gives the remainder. Floats remain useful for other measurements.

---

# Formatting turns a result into a readable message

Calculation and presentation have different jobs.

```python
amount_paise = 49905
label = f"₹{amount_paise // 100:,}.{amount_paise % 100:02d}"
print(label)
```

The display is ₹499.05; the stored amount is still an integer.

---

# Strings support searching and display preparation

An operation should match its purpose: trim accidental spaces and normalize case for comparison.

```python
query = "  CABLE  "
normalized_query = query.strip().casefold()
print(normalized_query in "USB-C Cable".casefold())
```

Retain the original product name for display.

---

# Comparisons produce decisions

Conditions turn application rules into Boolean expressions.

```python
quantity = 2
is_positive = quantity > 0
is_single_unit = quantity == 1
print(is_positive, is_single_unit)
```

`=` assigns a value; `==` compares two values.

---

# Branches select one path

Software changes behavior when a condition holds. Indentation defines the selected block.

```python
quantity = 0
if quantity > 0:
    message = "Ready to add"
else:
    message = "Choose a positive quantity"
print(message)
```

---

# Several conditions express a richer choice

Put specific conditions in an order that matches the rule.

```python
subtotal_paise = 99800
if subtotal_paise == 0:
    delivery_paise = 0
elif subtotal_paise >= 100000:
    delivery_paise = 0
else:
    delivery_paise = 5000
```

This delivery rule is a teaching experiment, separate from the supplied checkout.

---

# A function names a reusable transformation

A function makes an operation callable wherever its result is needed.

```python
def line_total(unit_price_paise, quantity):
    return unit_price_paise * quantity

print(line_total(49900, 2))
```

The parameter names describe roles; arguments supply actual values.

---

# Definition and invocation happen at different times

Defining a function creates a callable; calling it executes its body.

```python
def product_label(name):
    return f"Product: {name}"

label = product_label("USB-C Cable")
print(label)
```

Trace the call, the return, and the caller’s next line.

---

# Return makes a result available to other code

A returned value can feed another calculation, a message, or a later test.

```python
def line_total(price_paise, quantity):
    return price_paise * quantity

subtotal_paise = line_total(49900, 2)
order_total_paise = subtotal_paise + 5000
```

Printing alone cannot supply the number for this addition.

---

# Predict the result of a print-only function

Which values appear, and what is assigned to `result`?

```python
def show_total(price_paise, quantity):
    print(price_paise * quantity)

result = show_total(49900, 2)
print(result)
```

---

# A function without return supplies None

The first line displays **99800**; the second displays **None**.

```python
def calculate_total(price_paise, quantity):
    return price_paise * quantity

result = calculate_total(49900, 2)
print(result)
```

Keep display at the caller when a result must be reused.

---

# Local names keep an operation understandable

A function can calculate intermediate values without exposing them as application state.

```python
def money(amount_paise):
    rupees = amount_paise // 100
    remainder = amount_paise % 100
    return f"₹{rupees:,}.{remainder:02d}"

print(money(99800))
```

The caller receives the label, not the function’s local names.

---

# Composition builds larger behavior from smaller parts

Combine simple functions through their return values.

```python
def line_total(price_paise, quantity):
    return price_paise * quantity

def checkout_total(price_paise, quantity, delivery_paise):
    return line_total(price_paise, quantity) + delivery_paise

print(checkout_total(49900, 2, 5000))
```

---

# Comments explain the reason for a choice

Teach intent where the representation might otherwise be confusing.

```python
# Keep amounts in paise so calculations use whole-number units.
unit_price_paise = 49900
# The CLI decides how to display this reusable result.
line_total_paise = unit_price_paise * 2
```

Readable names carry the ordinary mechanics; comments carry the decision.

---

# Errors expose a broken assumption

Deliberate failure: the quantity text is not a whole number.

```python
quantity_text = "two"
quantity = int(quantity_text)
```

Read the exception type, message, and failing line. Expect `ValueError`; do not guess from the final printed output.

---

# Recovery changes the failed assumption

Use numeric text, then recompute the result.

```python
quantity_text = "2"
quantity = int(quantity_text)
print(49900 * quantity)
```

M2 will handle expected bad input without ending the command loop.

---

# A script begins fresh; a notebook can retain state

A script executes top to bottom in a new process. Notebook cells can run in any order.

```python
quantity = 2
subtotal_paise = 49900 * quantity
```

Changing `quantity` in a later cell does not refresh an already assigned subtotal. Restart the kernel and run all to reproduce the sequence.

---

# Codealong: change one fact and trace its effects

Open [the notebook](codealong.ipynb), exploration 1.

Start with price 49900 and quantity 2. Change quantity to 3, then price to 0.

Explain which results change and why. Keep the same function; change its arguments.

---

# Codealong: separate a calculation from its display

In exploration 2, complete the label function using `money` and a product name.

Compare a returned string with a print-only function. Capture each result in a variable.

Repair the deliberate conversion failure with a numeric string; explain what remains unvalidated.

---

# Expert review: choose an interface people can reuse

Review `print(price * quantity)` inside a calculator.

Would a CLI, HTTP handler, and test all be able to reuse its result? Choose a return value and leave presentation to the caller.

Explain what `int("-2")` accepts and why conversion alone does not enforce the shop’s quantity rule.

---

# Transfer: identify the same pieces in another feature

A discount needs inputs, an expression, a rule, and a returned result.

State those pieces before writing Python. Which values need names? Which condition rejects an input?

These mechanisms can express a different application without changing their meaning.

---

# Nano-Zon lab: apply the mechanism

Return money labels, product labels, and line totals.

Start from the independent [M1 starter](../../projects/nano-zon/labs/m01/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m01/README.md) and [answer map](../../projects/nano-zon/labs/m01/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
python3 shop.py
```

**Expected:** Two cables and one bottle total ₹1,897.00; successful checkout clears the cart.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Add a separate whole-percentage discount calculation; explain rounding down fractional paise.

The [lab guide](../../projects/nano-zon/labs/m01/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Trace inputs into results, choose behavior, and name a reusable calculation.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Process collections and manage changes.
