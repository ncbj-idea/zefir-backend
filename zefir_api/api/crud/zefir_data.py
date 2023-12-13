from typing import Callable, Final

from zefir_analytics import ZefirEngine

from zefir_api.api.crud.costs import (
    get_capex,
    get_ets,
    get_opex,
    get_total_costs,
    get_var_cost,
)
from zefir_api.api.crud.emissions_and_fuels import get_emissions, get_fuel_usage
from zefir_api.api.crud.energy_type_production import (
    get_cold_production,
    get_ee_production,
    get_heat_production,
)
from zefir_api.api.crud.energy_type_usage import (
    get_cold_usage,
    get_ee_usage,
    get_heat_usage,
)
from zefir_api.api.crud.power_and_devices import (
    get_increasing_amount_of_devices,
    get_installed_power,
)
from zefir_api.api.parameters import DataCategory
from zefir_api.api.payload.zefir_data import ZefirDataResponse

method_to_data_category_map: Final[
    dict[DataCategory, Callable[[ZefirEngine], ZefirDataResponse]]
] = {
    DataCategory.INSTALLED_POWER: get_installed_power,
    DataCategory.EE_PRODUCTION: get_ee_production,
    DataCategory.HEAT_PRODUCTION: get_heat_production,
    DataCategory.COLD_PRODUCTION: get_cold_production,
    DataCategory.EE_USAGE: get_ee_usage,
    DataCategory.HEAT_USAGE: get_heat_usage,
    DataCategory.COLD_USAGE: get_cold_usage,
    DataCategory.AMOUNT_OF_DEVICES: get_increasing_amount_of_devices,
    DataCategory.EMISSIONS: get_emissions,
    DataCategory.FUEL_USAGE: get_fuel_usage,
    DataCategory.CAPEX: get_capex,
    DataCategory.OPEX: get_opex,
    DataCategory.VAR_COST: get_var_cost,
    DataCategory.ETS: get_ets,
    DataCategory.TOTAL_COSTS: get_total_costs,
}
