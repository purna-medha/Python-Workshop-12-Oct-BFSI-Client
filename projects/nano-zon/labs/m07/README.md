# M7 — Express behavioral promises

Tests supply known inputs and compare observable outcomes with independently understood expectations. Boundary cases and fresh fixtures prevent a green result from depending on accidents or earlier test state.

**Start:** [starter/](starter/README.md). The application is complete through SQLite. Run `uv sync --extra dev`. Read `tests/conftest.py` to understand the supplied fresh cart and product fixtures.

## Complete the test bodies

In `tests/test_domain.py`, follow [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. Assert each parametrized line total against its expected result.
2. Use `pytest.raises` to establish rejected quantities with a narrow exception.
3. Check case-insensitive search, no matches, and the valid zero price bound.
4. Check that an order preserves its original quantities and prices after the cart changes.

Names, parameters, decorators, fixtures, and arrange/act sections are written. Other cart, empty-checkout, missing-product, and schema checks are supplied as examples. Remove the guard inside each completed test.

## Observe completion

```sh
uv run --extra dev pytest tests/test_domain.py -q
uv run --extra dev pytest tests/test_contracts.py -q
```

Pending regions deliberately fail rather than skip. Correct completed tests establish calculations, rejection, selection, ownership, and snapshots without a live server. Add one independently chosen case and explain why it provides additional evidence.

Temporarily introduce a small arithmetic defect in your own starter, inspect the failing assertion, then restore it. The failure should identify behavior rather than depend on a private helper's name.

**Explain:** Why is a known expected amount stronger than checking that the function returns an integer?

**Expert review:** Review fixture scope and test independence. Would the tests still establish the same behavior after a reasonable internal refactor?

## Independent extension — no supplied answer

Choose one application promise not exercised by your completed answer regions and write its test without copying a supplied assertion. Explain the expected outcome and one plausible defect it would catch.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Next:** [M8](../m08/README.md) checks real API/database collaboration and external failure behavior.
