# NCBR_backend
# Copyright (C) 2023-2024 Narodowe Centrum Badań Jądrowych
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime

from zefir_analytics import ZefirEngine

from zefir_api.api.config import params_config
from zefir_api.api.crud.costs import _calculate_ets_fee, _calculate_var_cost
from zefir_api.api.crud.utils import flatten_multiindex
from zefir_api.api.parameters import Area, Scenario
from zefir_api.api.payload.zefir_static import StaticScenarioDescriptionResponse
from zefir_api.api.zefir_engine import ze


def _get_time_of_result_creation(scenario_name: str, area_name: str) -> datetime:
    creation_time = (
        (params_config.get_result_path(area_name) / scenario_name).stat().st_ctime
    )
    return datetime.fromtimestamp(creation_time)


def generate_scenarios_description(
    area: Area,
) -> list[StaticScenarioDescriptionResponse]:
    return [
        generate_scenario_description(
            scenario=scenario, engine=ze[scenario.id], area_name=area.name
        )
        for scenario in area.scenarios
        if scenario.id in ze
    ]


def generate_scenario_description(
    scenario: Scenario,
    engine: ZefirEngine,
    area_name: str,
) -> StaticScenarioDescriptionResponse:
    capex_opex = engine.source_params.get_capex_opex(level="type")
    capex, opex = capex_opex[["capex"]], capex_opex[["opex"]]
    capex = flatten_multiindex(capex.dropna()).sum().sum()
    opex = flatten_multiindex(opex.dropna()).sum().sum()
    var_cost = _calculate_var_cost(engine).sum().sum()
    total_cost = capex + opex + var_cost + _calculate_ets_fee(engine).sum().sum()
    CO2_emissions = engine.source_params.get_emission(level="type")[["CO2"]].sum()
    return StaticScenarioDescriptionResponse(
        id=scenario.id,
        name=engine.scenario_name,
        total_cost=total_cost,
        total_capex=capex,
        total_opex=opex,
        total_varcost=var_cost,
        total_emission_CO2=CO2_emissions,
        date=_get_time_of_result_creation(engine.scenario_name, area_name),
        description=scenario.description,
        analyze_time=engine.network.constants.n_years,
        analyze_step=int(engine.network.constants.n_hours / 8760),
    )
