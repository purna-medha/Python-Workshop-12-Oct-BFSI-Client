# Executing code does not establish correctness. An assertion must distinguish
# valid behavior from plausible defects. Precise examples and boundary cases
# provide stronger evidence than checks that merely accept a result's type.
#
# Compare a type-only total check with exact totals and rejected quantities.

import pytest
from m09.pricing import calculate_line_total


def test_weak_example_only_checks_type():
    assert isinstance(calculate_line_total(49900, 2), int)


@pytest.mark.parametrize("price, quantity, expected", [
    (49900, 1, 49900), (49900, 2, 99800), (0, 2, 0),
])
def test_line_total_rule(price, quantity, expected):
    assert calculate_line_total(price, quantity) == expected


@pytest.mark.parametrize("quantity", [0, -1, True])
def test_invalid_quantity_is_rejected(quantity):
    with pytest.raises(ValueError, match="positive integer"):
        calculate_line_total(49900, quantity)

# Run: uv run --extra dev pytest m09/s02_assertion_quality.py -q
# Experiment: change pricing.py's multiplication to addition, then restore it.
# The weak check stays green; the meaningful checks detect the defect.
