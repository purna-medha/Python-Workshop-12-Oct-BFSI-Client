# Coverage records execution, revealing paths that examples have not reached.
# Line coverage asks which statements ran; branch coverage also asks which
# outcomes of decisions ran. Neither establishes the strength of assertions.
#
# Start with one accepted quantity, then inspect the unchecked rejection path.

from m09.pricing import calculate_line_total


def test_two_cables_cost_99800_paise():
    assert calculate_line_total(49900, 2) == 99800


# Run from current-course/teaching-snippets:
# uv run --extra dev pytest m09/s01_coverage_paths.py \
#   --cov=m09.pricing --cov-branch --cov-report=term-missing
# The rejected-quantity path remains uncovered; try zero, negative, and Boolean.
# Branch reporting also exposes decisions exercised in only one direction.
# Add cases yourself, then compare with snippet 02's stronger tests.
