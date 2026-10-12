---
marp: true
theme: default
paginate: true
size: 16:9
title: "M9 · Maintain useful evidence as software changes"
description: "Python application development through Pico-Zon and Nano-Zon"
style: |
  section { font-family: Arial, sans-serif; font-size: 25px; line-height: 1.25; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 21px; line-height: 1.2; background: #f1f5f9; }
  code { color: #0f172a; }
  a { color: #0369a1; }
  strong { color: #164e63; }
---
# M9 · Maintain useful evidence as software changes

Use coverage to find gaps, strengthen assertions, and repeat the same checks locally and in CI.

**Pico-Zon:** explore the mechanism. **Nano-Zon:** apply it in the lab.

---

# Every new capability grows the same shop

Values → collections → owned records → HTTP → contracts → persistence → tests → integration → CI.

Today’s examples isolate one mechanism; the application reconnects it to the whole.

---

# A green suite still has a limited claim

Every check exercises selected inputs and selected comparisons.

```text
What ran?      coverage
What matched?  assertions
What stayed repeatable? setup and dependencies
```

Confidence grows when these kinds of evidence support a specific behavioral promise.

---

# Coverage observes execution

Coverage can reveal a path that no test exercised.

```python
def line_total(price_paise, quantity):
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be positive")
    return price_paise * quantity
```

An ordinary two-unit test does not execute the rejection statement.

---

# Line coverage and branch coverage ask different questions

A visited condition line can still have an unvisited outcome.

```text
quantity accepted → return result
quantity rejected → raise error
```

Line coverage tracks statements executed. Branch coverage tracks alternative control-flow destinations.

---

# Run coverage over the behavior you intend to inspect

From a Nano-Zon starter with the declared dev dependencies:

```sh
uv run --extra dev pytest --cov=nanozon --cov-branch --cov-report=term-missing
```

`nanozon` is the application under inspection. Do not use a percentage over unrelated files to support a different claim.

---

# Read the missing locations as questions

A report’s Missing column identifies statements or branch destinations to investigate.

```text
Missing rejection path → which invalid input reaches it?
Missing zero bound     → does absence differ from zero?
```

Inspect the code and requirement before choosing a test. A report does not tell you the correct expected outcome.

---

# Predict whether execution exposes the defect

A suite exercises every line of a simple calculator but only checks its result type.

```python
actual = 49900 + 2  # Deliberate arithmetic defect
assert isinstance(actual, int)
```

Will coverage or this assertion reject the defect?

---

# An executed line can produce an unexamined wrong result

The type assertion passes. Coverage can record that the arithmetic line ran without judging its meaning.

```python
assert actual == 99800  # Fails for the deliberate addition result
```

The expected amount supplies the behavioral evidence.

---

# Strengthen the comparison before chasing a target

The shop’s promise is multiplication for the given quantity.

```python
from m09.pricing import calculate_line_total

def test_two_cables_cost_99800():
    assert calculate_line_total(49900, 2) == 99800
```

A coverage threshold cannot replace this assertion.

---

# Choose a missing branch by its rule

A zero quantity must take the rejection path.

```python
import pytest

def test_zero_quantity_rejected():
    with pytest.raises(ValueError):
        calculate_line_total(49900, 0)
```

This tests a meaningful rule and extends execution evidence at the same time.

---

# A zero price bound exposes an omission bug

A truthiness check would treat zero as if no bound had been supplied.

```python
maximum_paise = 0
apply_filter = maximum_paise is not None
assert apply_filter is True
```

The Nano-Zon lab checks the public search result, not only this isolated condition.

---

# A deliberate mutation reveals assertion quality

In your own copy, temporarily replace multiplication with addition.

```text
Weak type assertion → still green
Exact amount check  → failure expected
Restore the implementation afterward
```

This is a focused defect experiment; it is not a claim that every possible defect is detected.

---

# Small changes can reveal a missing boundary

Test the smallest accepted quantity, then the nearest rejected one.

```python
assert calculate_line_total(49900, 1) == 49900
with pytest.raises(ValueError):
    calculate_line_total(49900, 0)
```

The pair explains the accepted boundary more clearly than arbitrary additional amounts.

---

# Deterministic checks control their changing inputs

A test should fail because behavior changed, not because an unrelated clock or network did.

```text
Fresh cart        known starting state
Temporary file    isolated storage
Controlled HTTP   repeatable external outcome
```

Use generated order IDs by relationship and shape, not by assuming a fixed UUID.

---

# An assertion can validate a variable identity meaningfully

Capture the returned ID, then use it for retrieval.

```python
order_id = created.json()["order_id"]
assert isinstance(order_id, str) and order_id
retrieved = client.get(f"/orders/{order_id}")
assert retrieved.json()["order_id"] == order_id
```

Here a type/shape assertion has a role; exact totals still need exact arithmetic assertions.

---

# Diagnostics should identify the violated promise

Keep each assertion close to the behavior it examines.

```python
assert order.total_paise == 99800, "Two cables must use checkout-time prices"
```

A useful failure helps distinguish input setup, domain behavior, and persistence. Avoid catching a failed assertion and continuing as if the suite passed.

---

# Repeatable commands begin with a known environment

Choose the classroom Python version and declared dependency set.

```sh
uv sync --extra dev
uv run --extra dev python -m m09.s03_repeatable_checks
```

From teaching-snippets: the supplied runner uses Python’s active interpreter and project configuration.

---

# One runner keeps local and CI intent aligned

A shared entry point avoids maintaining two different test selections.

```python
import subprocess, sys
result = subprocess.run(
    [sys.executable, "-m", "pytest", "--cov-branch"],
    check=False,
)
raise SystemExit(result.returncode)
```

Focused runner example. The supplied runner also sets targets, report paths, and working directory.

---

# A failed check must retain its failure status

Automation relies on the process result to stop a green claim.

```text
pytest failure → nonzero exit → runner forwards it → CI fails
```

A script that always exits zero can hide failures even while printing an error message.

---

# Reports preserve evidence for later inspection

Console output helps now; machine-readable files help after a remote run.

```text
reports/tests.xml     test outcomes
reports/coverage.xml  execution coverage
term-missing          immediate local gaps
```

The supplied teaching runner creates these reports; the workflow retains them after failures too.

---

# CI starts from a clean checkout

A workflow repeats installation and checks in an independent environment.

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"
```

Excerpt from the supplied template. The runner cannot depend on a developer’s already installed local packages.

---

# Install the dependencies the checks actually need

Project metadata is part of the runnable contract.

```yaml
- name: Install dependencies
  run: python -m pip install -e ".[dev]"
- name: Run checks
  run: python -m m09.s03_repeatable_checks
```

Teaching-snippets template excerpt. Keep its working directory set to `teaching-snippets`.

---

# Retain reports even when tests fail

Failed checks are often when the reports are most valuable.

```yaml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: python-check-reports
    path: teaching-snippets/reports/
```

Excerpt from the template; paths are relative to the repository checkout for this action.

---

# A template is not an active workflow

GitHub discovers workflows under `.github/workflows/` in the intended repository.

Nano-Zon’s template assumes its application is at the repository root. A nested teaching checkout needs adjusted working directories and report paths.

Installing a workflow does not configure branch protection or required checks automatically.

---

# Codealong: expose a green but weak check

Open [the notebook](codealong.ipynb), exploration 1.

Run the local broken calculation against a type-only check, then an exact amount check.

Explain what coverage would observe and what only the assertion can establish.

---

# Codealong: investigate one gap and inspect the runner

In exploration 2, choose a boundary case and state its expected behavior.

Read the supplied runner and CI template. Match interpreter, dependencies, test selection, exit status, and report location.

The notebook does not launch pytest or activate CI automatically.

---

# Expert review: choose useful gates

A percentage can identify a regression in execution, but cannot measure assertion quality by itself.

Explain one plausible defect the suite still misses before proposing a coverage threshold.

Optional: formatters standardize presentation; linters find selected patterns; type checkers examine annotated interfaces. Each has a different claim.

---

# Complete the shop and explain a failed operation

Demonstrate browse → cart → simulated order → restart → retrieval.

Trace a rejected quantity and a controlled storage failure. Explain where each rule, translation, and evidence belongs.

The final application combines ordinary language mechanisms with interfaces, persistence, and automated checks.

---

# Transfer: prepare a foundation for the next feature

Identify an ordinary callable operation, its accepted input shape, and its returned result.

Describe which tests establish the promise and which failures the caller must handle.

Those explicit operations and contracts can support a later AI interface; Day 4 is a separate course design.

---

# Nano-Zon lab: apply the mechanism

Strengthen a weak assertion, cover zero-bound behavior, and complete coverage/CI configuration.

Start from the independent [M9 starter](../../projects/nano-zon/labs/m09/starter/README.md); earlier core work is supplied. Follow the [lab guide](../../projects/nano-zon/labs/m09/README.md) and [answer map](../../projects/nano-zon/labs/m09/starter/ANSWER-MAP.md).

Write or uncomment the selected answers and remove their matching guards. The supplied wiring keeps focus on this module’s new capability.

---

# Observe the promised behavior

From this module’s Nano-Zon starter folder:

```sh
uv run --extra dev pytest --cov=nanozon --cov-branch --cov-report=term-missing
```

**Expected:** Explain a detected defect and a remaining gap; review CI commands and retained reports.

Follow the lab guide for dependency setup, required services, and additional checks. A pending-region counter reports unfinished edits; it does not establish correctness.

---

# Independent practice: make and explain a decision

Choose an uncovered path or weak assertion; write a check and name the defect it detects.

The [lab guide](../../projects/nano-zon/labs/m09/README.md) defines this unsupplied extension. State its input, output, and one case that distinguishes correct from incorrect behavior.

Personal extensions remain in your copy; the next starter supplies the shared core.

---

# Explain the mechanism without quoting the syntax

Use coverage to find gaps, strengthen assertions, and repeat the same checks locally and in CI.

Name the general principle, the shop problem it solves, and one limit of its guarantee. Then point to the Python that expresses it.

You can now trace a shopping operation through rules, interfaces, storage, and evidence. Use the same reasoning for your next application.
