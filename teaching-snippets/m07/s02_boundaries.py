# A behavior contract covers ordinary success, boundaries, and rejected inputs.
# Expected exceptions are observable outcomes too. Narrow exception assertions
# prevent unrelated defects from accidentally satisfying a failure check.
#
# Establish checkout rules for empty selections, invalid quantities, and missing IDs.

import pytest
from m03.shop import calculate_line_total, create_order


def test_free_product_can_have_zero_price():
    assert calculate_line_total(0, 1) == 0


def test_zero_quantity_is_rejected():
    with pytest.raises(ValueError, match="positive integer"):
        calculate_line_total(49900, 0)


def test_empty_checkout_is_rejected():
    with pytest.raises(ValueError, match="empty cart"):
        create_order([])


def test_unknown_product_is_rejected():
    with pytest.raises(KeyError) as captured:
        create_order([("999", 1)])
    assert captured.value.args == ("999",)

# Run: uv run --extra dev pytest m07/s02_boundaries.py -q
# Zero price and zero quantity mean different things; rules follow the domain.
