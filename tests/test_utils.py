"""
Tests for utility functions
"""

from pytest import raises
from src.utils import get_month_range, count_months, to_float
from src.errors import InternalError
from data.constants import CZECH_MONTHS

def test_get_month_range_normal_case():
    """Test get_month_range."""
    assert get_month_range(4, 7, CZECH_MONTHS) == ["duben", "květen", "červen"] #start <= end
    assert get_month_range(11, 2, CZECH_MONTHS) == ["listopad", "prosinec", "leden"] #start > end
    assert get_month_range(5, 5, CZECH_MONTHS) == ["květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec", "leden", "únor", "březen", "duben"] #same month
    assert not get_month_range(5, 5, CZECH_MONTHS, mark=2)  # same month


def test_count_months_same_month():
    """Test count_months."""
    assert count_months(12, 12) == 12 #start == end
    assert count_months(1, 5) == 4 #start < end
    assert count_months(3, 7) == 4
    assert count_months(10, 2) == 4 # start > end
    assert count_months(12, 1) == 1


def test_to_float_valid_inputs():
    """Test to_float with valid number strings."""
    assert to_float("123")==123.0
    assert to_float("123.45")==123.45
    assert to_float("123,45")== 123.45
    assert to_float("-123,45")==-123.45


def test_to_float_invalid_inputs():
    """Test to_float with invalid inputs."""
    with raises(InternalError, match="⚠️Not a number"):
        to_float("abc")

    with raises(InternalError, match="⚠️Not a number"):
        to_float("12a34")

    with raises(InternalError, match="⚠️Not a number"):
        to_float("")
