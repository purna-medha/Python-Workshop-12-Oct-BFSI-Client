# A test supplies inputs, performs an operation, and checks an independently
# understood result. Assertions establish behavior rather than merely execute
# code. A useful failure identifies the mismatch between promise and outcome.
#
# Capture the promise that a line total is unit price multiplied by quantity.

from m03.shop import calculate_line_total


def test_two_cables_cost_99800_paise():
    unit_price_paise = 49900        # Arrange known inputs.
    quantity = 2
    total_paise = calculate_line_total(unit_price_paise, quantity)  # Act.
    assert total_paise == 99800     # Assert an independently calculated answer.


def test_one_bottle_costs_89900_paise():
    assert calculate_line_total(89900, 1) == 89900


# Run: uv run --extra dev pytest m07/s01_assertions.py -q
# Experiment: temporarily change * to + in shop.py, read the failure, then restore.
# Comparing the function with another call to itself would not establish correctness.
