# Several examples can establish one rule without duplicating test structure.
# Parametrization makes each case independently reported, so one failing
# boundary can be identified even when other cases still succeed.
#
# Exercise monetary calculations and quantity validation across representative inputs.

import pytest
from m03.shop import calculate_line_total


@pytest.mark.parametrize("price, quantity, expected", [
    pytest.param(49900, 1, 49900, id="one-cable"),
    pytest.param(49900, 2, 99800, id="two-cables"),
    pytest.param(89900, 3, 269700, id="three-bottles"),
    pytest.param(0, 2, 0, id="free-product"),
])
def test_line_total(price, quantity, expected):
    assert calculate_line_total(price, quantity) == expected


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_quantity_must_be_a_positive_integer(quantity):
    with pytest.raises(ValueError, match="positive integer"):
        calculate_line_total(49900, quantity)

# Run: uv run --extra dev pytest m07/s03_parametrization.py -q
# Add a new case by adding data. True is excluded despite bool being an int subclass.
