"""
Module for calculating electricity costs and performing tariff-based recalculations.
"""

from dataclasses import dataclass, field
from src.storage import load_data
from src.errors import InternalError

@dataclass
class TariffConstants:
    """
    Fixed constants for electricity tariff calculation.
    """
    tax_per_mwh: float = 28.30
    system_services_per_mwh: float = 170.92
    infrastructure_fee: float = 2.89
    poze_per_mwh: float = 495


@dataclass
class TariffConfig:
    """
    Configuration data for electricity tariff calculations.
    """
    energy_price_per_kwh: float
    fixed_supplier_fee: float
    high_tariff_mwh: float
    low_tariff_mwh: float
    high_tariff_ratio: float
    breaker_fee: float
    constants: TariffConstants = field(default_factory=TariffConstants)

def fixed_fees(config: TariffConfig, month_count):
    """
    Calculates total fixed fees based on input values and month count.
    """
    return (config.fixed_supplier_fee+config.breaker_fee+config.constants.infrastructure_fee)*month_count

def recalculation(file):
    """
    Recalculates the total difference from stored graph data.
    """
    data=load_data(file)
    if not data:
        raise InternalError(f"⚠️File '{file}' is empty")
    costs=[entry["diff"] for entry in data]
    result=sum(costs)
    return result

def yearly_recalculation(file):
    """
    Estimates yearly cost based on average of current recalculated months.
    """
    data=load_data(file)
    if not data:
        raise InternalError(f"⚠️File '{file}' is empty")
    actual_recalculation=recalculation(file)
    average_cost=actual_recalculation/len(data)
    result=round(average_cost*12,2)
    return result


def calculate_tariff(month_count,
                     consumption_kwh,
                     config: TariffConfig
                     ):
    """
    Calculates the total electricity bill based on provided tariff and consumption data.
    """
    consumption_mwh=consumption_kwh/1000
    #supplier
    energy_cost=consumption_kwh*config.energy_price_per_kwh

    #distribution
    consumption_high_tariff=consumption_mwh*config.high_tariff_ratio
    consumption_low_tariff=consumption_mwh*(1-config.high_tariff_ratio)
    high_tariff_cost=consumption_high_tariff*config.high_tariff_mwh
    low_tariff_cost=consumption_low_tariff*config.low_tariff_mwh
    total_distribution=high_tariff_cost+low_tariff_cost

    #other
    tax_cost=consumption_mwh*config.constants.tax_per_mwh
    system_cost=consumption_mwh*config.constants.system_services_per_mwh
    poze_cost=consumption_mwh*config.constants.poze_per_mwh
    total_other=round(tax_cost+system_cost+poze_cost,2)

    if consumption_kwh==0:
        total=0
    else:
        total = (energy_cost + total_distribution + total_other + fixed_fees(config, month_count))*1.21
    return round(total,2)
