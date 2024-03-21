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

import json
from pathlib import Path
from typing import Final

from zefir_analytics import ZefirEngine

from zefir_api.api.config import params_config
from zefir_api.api.parameters import Area, Scenario

AREA_MAP = dict[int, Area]


def load_area_scenario_mapping(mapping_filepath: Path) -> AREA_MAP:
    with open(mapping_filepath) as f:
        return create_area_scenario_mapping(json.load(f))


def create_area_scenario_mapping(area_json: dict) -> AREA_MAP:
    result_dict = {}
    scenario_id_count = 0
    for area_id, area_name in enumerate(area_json):
        scenarios = []
        for scenario in area_json[area_name]:
            scenarios.append(
                Scenario(
                    id=scenario_id_count,
                    name=scenario["scenario_name"],
                    description=scenario["description"],
                )
            )
            scenario_id_count += 1

        area = Area(id=area_id, name=area_name, scenarios=tuple(scenarios))
        result_dict[area_id] = area

    return result_dict


def create_zefir_engines(area_scenario_map: AREA_MAP) -> dict[int, ZefirEngine]:
    return {
        scenario.id: ZefirEngine.create_from_config(
            params_config.get_config_path(area.name, scenario.name)
        )
        for area in area_scenario_map.values()
        for scenario in area.scenarios
    }


area_scenario_mapping: Final[AREA_MAP] = load_area_scenario_mapping(
    params_config.areas_mapping_filepath
)
ze: Final = create_zefir_engines(area_scenario_mapping)


def get_scenario_id(scenario_name: str) -> int:
    for area in area_scenario_mapping.values():
        for scenario in area.scenarios:
            if scenario.name == scenario_name:
                return scenario.id
    raise ValueError(f"Scenario {scenario_name} not found")
