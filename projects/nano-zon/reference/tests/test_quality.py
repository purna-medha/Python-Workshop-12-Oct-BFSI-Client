# M9: meaningful assertions distinguish correct results from plausible defects.
import pytest
from nanozon.calculations import calculate_line_total
from nanozon.catalog import select_products


def test_weak_example_only_checks_type():
    assert isinstance(calculate_line_total(49900, 2), int)


def test_precise_total_detects_wrong_arithmetic():
    result = calculate_line_total(49900, 2)
    # ANSWER m09 strong_assertion BEGIN
    assert result == 99800
    # ANSWER m09 strong_assertion END


def test_price_filter_includes_its_boundary(products):
    # ANSWER m09 boundary_branch BEGIN
    assert [p.product_id for p in select_products(products, maximum_paise=49900)] == ["1"]
    assert select_products(products, maximum_paise=49899) == []
    assert select_products(products, maximum_paise=0) == []
    # ANSWER m09 boundary_branch END


def test_reversed_bounds_are_rejected(products):
    with pytest.raises(ValueError, match="Minimum"):
        select_products(products, minimum_paise=90000, maximum_paise=49900)
