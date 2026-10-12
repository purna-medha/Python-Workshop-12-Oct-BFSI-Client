---
marp: true
theme: default
paginate: true
size: 16:9
title: "M7 · Express behavioral promises as tests"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M7 · Express behavioral promises as tests

Check independently understood outcomes, boundaries, and fresh state with pytest.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# A test makes a promise executable

Known inputs and an independently understood result let a check detect a disagreement.

```python
from m03.shop import calculate_line_total

def test_two_cables_cost_99800_paise():
    assert calculate_line_total(49900, 2) == 99800
```

The expected amount is computed from the requirement, not another call to the same function.

---

# Discovery determines which checks run

Pytest finds test functions in matching files and executes them.

From `teaching-snippets/`:

```sh
uv sync --extra dev
uv run --extra dev pytest m07/s01_assertions.py -q
```

This project explicitly discovers `s*.py`. Running a file as a script only defines its test functions.

---

# Arrange, act, assert exposes the evidence

Separate input setup, the operation, and the comparison.

```python
def test_two_cables():
    price_paise = 49900
    quantity = 2
    actual = calculate_line_total(price_paise, quantity)
    assert actual == 99800
```

Each section answers a different question: starting facts, behavior, and expected outcome.

---

# Assertions should name the observable promise

A successful function call alone does not establish a correct result.

```python
actual = calculate_line_total(49900, 2)
assert actual == 99800
```

Compare a value, state change, or precise error that matters to a caller.

---

# Predict which check catches an arithmetic defect

Imagine multiplication is accidentally replaced with addition.

```python
assert isinstance(calculate_line_total(49900, 2), int)
assert calculate_line_total(49900, 2) == 99800
```

Which assertion still passes? Which one gives evidence of the violated rule?

---

# A check is useful when wrong behavior makes it fail

The type-only assertion still passes for integer 49902. The exact amount assertion fails.

Inspect actual versus expected, then locate the calculation. Restore multiplication and keep the behavioral test.

A green assertion establishes only the promise it actually compares.

---

# One ordinary case leaves many rules unexamined

Choose cases by meaning rather than by quantity of test functions.

```text
one unit       smallest accepted quantity
two units      exposes multiplication versus addition
zero price     legitimate free product
zero quantity  rejected request
```

Price zero and quantity zero carry different domain meanings.

---

# Empty input can be valid for one operation and invalid for another

An empty subtotal can be zero while empty checkout is rejected.

```python
import pytest
from m03.shop import create_order

def test_empty_checkout_is_rejected():
    with pytest.raises(ValueError, match="empty cart"):
        create_order([])
```

Test each operation’s public promise.

---

# Expected errors are observable outcomes

A precise exception assertion distinguishes rejection from an unrelated defect.

```python
def test_zero_quantity_is_rejected():
    with pytest.raises(ValueError, match="positive integer"):
        calculate_line_total(49900, 0)
```

`pytest.raises(Exception)` could accept an accidental `NameError` and hide the real problem.

---

# Inspect an error’s data when it matters

A missing product should identify the requested ID.

```python
def test_unknown_product_is_rejected():
    with pytest.raises(KeyError) as captured:
        create_order([("999", 1)])
    assert captured.value.args == ("999",)
```

Avoid exact full traceback assertions; frame formatting is not the domain contract.

---

# Parametrization shares structure without merging results

Different cases can check one rule while remaining independently reported.

```python
@pytest.mark.parametrize("price, quantity, expected", [
    (49900, 1, 49900),
    (49900, 2, 99800),
    (0, 2, 0),
])
def test_line_total(price, quantity, expected):
    assert calculate_line_total(price, quantity) == expected
```

Each row supplies a separate test case.

---

# Case names improve failure diagnosis

A reader should recognize which boundary failed.

```python
case = pytest.param(49900, 2, 99800, id="two-cables")
```

Use it in the preceding case list. Prefer a meaningful case label over a label that repeats implementation details.

---

# Reject the nearby invalid values

Boundaries are where a broad implementation often disagrees with the rule.

```python
@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_quantity_must_be_positive_integer(quantity):
    with pytest.raises(ValueError):
        calculate_line_total(49900, quantity)
```

Include Boolean quantity deliberately: Python’s numeric inheritance does not decide this shopping rule.

---

# Fresh setup makes each test independent

A fixture supplies known starting state for each test that asks for it.

```python
from m03.cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()
```

Pytest resolves the fixture by the test parameter name.

---

# A test should not inherit a previous test’s cart

Two independent instances expose shared-state defects.

```python
def test_carts_are_independent(cart):
    other = ShoppingCart()
    cart.add("1", 2)
    assert cart.quantities == {"1": 2}
    assert other.quantities == {}
```

Run alone or in a different order: the intended starting conditions stay the same.

---

# Shared setup belongs in a small conftest module

Put reusable fixtures in `conftest.py` near the tests that use them.

```text
m07/
  conftest.py                    fresh cart fixture
  s01_assertions.py              known amounts
  s04_isolation_and_regression.py ownership and snapshots
```

Tests request fixtures; they do not import and invoke fixture functions directly.

---

# Test both the result and the state transition

Checkout supplies an order and clears the successful draft.

```python
def test_checkout_clears_cart(cart):
    cart.add("1", 2)
    order = cart.checkout()
    assert order.total_paise == 99800
    assert cart.quantities == {}
```

A correct total alone would not expose forgotten clearing.

---

# Snapshots need evidence after later changes

A historical promise becomes visible when current state changes.

```python
def test_order_preserves_quantity(cart):
    cart.add("1", 2)
    order = cart.checkout()
    cart.add("1", 5)
    assert order.lines[0].quantity == 2
    assert order.total_paise == 99800
```

Checking only immediately after checkout would miss a live-reference defect.

---

# A regression test retains the violated promise

After a defect is found, choose the smallest input that exposes it.

```text
Observe wrong result → write an assertion that fails
                     → repair behavior → retain the test
```

Keep the test about public behavior so a reasonable internal refactor can preserve it.

---

# Failure output connects an expectation to actual behavior

An assertion failure shows which test and comparison disagree.

```text
Expected: 99800
Actual:   49902
Likely question: was multiplication replaced by addition?
```

This is illustrative failure evidence, not captured output from a run in this session.

---

# Select a small check while investigating

Narrow feedback helps locate a defect without discarding the full suite.

```sh
uv run --extra dev pytest m07 -k quantity -q
uv run --extra dev pytest m07/s01_assertions.py::test_two_cables_cost_99800_paise -q
```

Run the broader relevant suite after the local repair.

---

# Do not compute the expected result through the implementation

A self-comparison can remain green through the same defect.

```python
# Weak: both sides run the implementation under test.
assert calculate_line_total(49900, 2) == calculate_line_total(49900, 2)
```

A requirement-derived amount of 99800 establishes a different and useful comparison.

---

# Codealong: write the promise before executing it

Open [the notebook](codealong.ipynb), exploration 1.

Write a test for two cables and one for zero price. Predict the assertion result.

Notebook cells define tests; use the supplied pytest command to exercise discovery and reporting.

---

# Codealong: introduce and recover from a controlled defect

In exploration 2, compare a small broken local calculation with the correct one.

Explain why the two-unit case exposes it. Keep the repository implementation intact during notebook exploration.

For a deliberate file edit in your own copy, restore the implementation after reading the failure.

---

# Expert review: keep assertions independent of mechanics

Would renaming a private helper or changing a loop to a comprehension break the test?

Prefer the returned total, observable cart state, historical facts, and specific rejection.

Choose one valid behavior a type-only assertion could not establish.

---

# Transfer: derive cases from a new promise

Choose case-insensitive catalog search.

State ordinary match, uppercase query, no match, and empty query expectations before writing tests.

The test design comes from the interface promise; pytest supplies its Python expression.

---

# Nano-Zon lab: apply the mechanism

Complete calculation, rejection, search, and snapshot assertions.

Start from the independent [M7 starter](../../projects/nano-zon/labs/m07/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m07/README.md) and [answer map](../../projects/nano-zon/labs/m07/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
uv run --extra dev pytest tests/test_domain.py tests/test_contracts.py -q
```

**Expected:** The selected assertions detect wrong totals and state leakage; pending regions deliberately fail.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Choose another public promise and write a test with an independent expected outcome.

The [lab guide](../../projects/nano-zon/labs/m07/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Check independently understood outcomes, boundaries, and fresh state with pytest.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

Next: Establish component collaboration.
