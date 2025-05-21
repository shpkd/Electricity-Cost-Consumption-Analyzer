"""
Module for testing functions from calculate.py.
"""

import tempfile
import os
import pytest
from src.calculate import yearly_recalculation, calculate_tariff, recalculation, fixed_fees, TariffConfig
from src.errors import InternalError
from src.storage import save_data_append, save_data

config = TariffConfig(
        energy_price_per_kwh=5.0,
        fixed_supplier_fee=100,
        high_tariff_mwh=1000,
        low_tariff_mwh=500,
        high_tariff_ratio=0.5,
        breaker_fee=50
    )

def test_calculate_tariff_basic():
    """Test basic electricity tariff calculation."""

    total = calculate_tariff(
        month_count=2,
        consumption_kwh=200,
        config=config
    )
    assert isinstance(total, float)
    assert total == 1929.49


def test_calculate_tariff_zero_consumption():
    """Test tariff calculation with zero consumption."""
    total = calculate_tariff(
        month_count=1,
        consumption_kwh=0,
        config=config
    )
    assert total == 0


def test_fixed_fees_basic():
    """Test basic calculation of fixed fees."""
    result = fixed_fees(config, 2)
    assert result == 305.78


def test_fixed_fees_zero_months():
    """Test fixed fees calculation with zero months."""
    result = fixed_fees(config, 0)
    assert result == 0


def test_recalculation_with_data():
    """Test recalculation on valid data file."""
    data = [
        {"diff": 10},
        {"diff": -5},
        {"diff": 15}
    ]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        save_data(data, tmp.name)
    try:
        assert recalculation(tmp.name) == 20
    finally:
        os.remove(tmp.name)


def test_recalculation_empty_file():
    """Test that recalculation raises an error on empty data."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(b"[]")
        tmp.close()
        with pytest.raises(InternalError):
            recalculation(tmp.name)
        os.remove(tmp.name)


def test_yearly_recalculation_empty_file():
    """Test that yearly_recalculation raises an error on empty data."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(b"[]")
        tmp.close()
        with pytest.raises(InternalError):
            yearly_recalculation(tmp.name)
        os.remove(tmp.name)


def test_yearly_recalculation_consistency():
    """
    Tests that yearly_recalculation returns the same value
    regardless of the number of identical monthly entries,
    as long as their average remains constant.
    """
    data = {
        "diff": -100,
        "cost": 100,
        "month": "-",
        "source": "user"
    }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp1, \
            tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp2:
        c1 = 0
        c2 = 0
        while c1 < 3:
            save_data_append(data, tmp1.name)
            c1 += 1
        while c2 < 11:
            save_data_append(data, tmp2.name)
            c2 += 1
    try:
        result1 = yearly_recalculation(tmp1.name)
        result2 = yearly_recalculation(tmp2.name)
        assert result1 == result2
    finally:
        os.remove(tmp1.name)
        os.remove(tmp2.name)


def test_yearly_recalculation_matches_calculate_tariff():
    """
    Test that yearly_recalculation(with less than 12 entries) is equal to calculate_tariff for a full year
    when using identical entries with the same diff value.
    """
    monthly_total = calculate_tariff(
        month_count=1,
        consumption_kwh=300,
        config=config
    )

    monthly_charge = 500
    monthly_diff = monthly_charge-monthly_total

    data = {
        "diff": monthly_diff,
        "cost": monthly_total,
        "month": "-",
        "source": "user"
    }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        c = 0
        while c < 3:
            save_data_append(data, tmp.name)
            c += 1
    try:
        result = yearly_recalculation(tmp.name)
        expected = round(monthly_diff * 12,2)
        assert result == expected
    finally:
        os.remove(tmp.name)


def test_yearly_recalculation_with_varying_diffs():
    """Test yearly_recalculation with varying diff values."""
    diffs = [-50, -100, -150]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        for diff in diffs:
            data = {
                "diff": diff,
                "cost": 100,
                "month": "-",
                "source": "user"
            }
            save_data_append(data, tmp.name)
    try:
        result = yearly_recalculation(tmp.name)
        expected = -100 * 12
        assert result == expected
    finally:
        os.remove(tmp.name)


def test_yearly_recalculation_with_exact_12_months():
    """Test yearly_recalculation with exactly 12 months of data."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        for i in range(12):
            data = {
                "diff": -100,
                "cost": 100,
                "month": f"2023-{i + 1}",
                "source": "user"
            }
            save_data_append(data, tmp.name)

    try:
        result = yearly_recalculation(tmp.name)
        expected = -100 * 12
        assert result == expected
    finally:
        os.remove(tmp.name)


def test_end_to_end_calculation():
    """Test end-to-end flow from calculate_tariff to recalculation."""
    tariff1 = calculate_tariff(
        month_count=1,
        consumption_kwh=200,
        config=config
    )

    config2=TariffConfig(
        energy_price_per_kwh=4.0,
        fixed_supplier_fee=90,
        high_tariff_mwh=800,
        low_tariff_mwh=600,
        high_tariff_ratio=0.6,
        breaker_fee=40
    )
    tariff2 = calculate_tariff(
        month_count=1,
        consumption_kwh=300,
        config=config2
    )

    #Create a data file with these values and some random diffs
    data = [
        {"diff": 50, "cost": tariff1, "month": "2023-01", "source": "user"},
        {"diff": -30, "cost": tariff2, "month": "2023-02", "source": "user"}
    ]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        save_data(data, tmp.name)

    try:
        #Test recalculation with this data
        recalc_result = recalculation(tmp.name)
        assert recalc_result == 20

        #Test yearly recalculation with this data
        yearly_result = yearly_recalculation(tmp.name)
        assert yearly_result == 20 * 6
    finally:
        os.remove(tmp.name)
