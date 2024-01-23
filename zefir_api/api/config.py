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

import configparser
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from zefir_api.api.utils import get_resources


@dataclass(frozen=True)
class ConfigParams:
    source_path: Path = get_resources("source_csv")
    result_path: Path = get_resources("results")
    parameter_path: Path = get_resources("parameters")
    polygons_file_path: Path = get_resources("map/polygonsFeatures.csv")
    fuel_units_path: Path = get_resources("static_data/fuel_units.json")
    plots_path: Path = get_resources("static_data/static_plots")
    aggregate_data_path: Path = get_resources("static_data/static_aggr_data")
    scenario_description_path: Path = get_resources(
        "static_data/scenarios_description.json"
    )
    transport_path: Path = get_resources("transport")
    points_file_path: Path = get_resources("map/pointsFeatures.csv")
    translate_tags_path: Path = get_resources("translation/tags_translation.json")
    translate_names_path: Path = get_resources("translation/names_translation.json")
    translate_fuels_path: Path = get_resources("translation/fuel_translation.json")
    translate_lbs_path: Path = get_resources("translation/lbs_translation.json")
    translate_energy_path: Path = get_resources("translation/energy_translation.json")
    tags_to_drop: list[str] = field(
        default_factory=lambda: ["KSE", "KSE_CONN", "HD_CONN"]
    )
    production_ee_name: str = "EE"
    production_heat_name: str = "HEAT"
    production_cold_name: str = "COLD"
    usage_ee_name: str = "EE"
    usage_heat_name: str = "HEAT"
    usage_cold_name: str = "COLD"


class ConfigParser:
    @staticmethod
    def load_config(config_file_path: str | None = None) -> ConfigParams:
        if config_file_path is None:
            return ConfigParams()
        config = configparser.ConfigParser()
        config.read(Path(config_file_path))
        config_dict: dict = {}
        for section in ["names", "paths", "tags"]:
            if config.has_section(section):
                config_dict.update(
                    (
                        key,
                        Path(value)
                        if section == "paths"
                        else value.split("-")
                        if section == "tags"
                        else value,
                    )
                    for key, value in config.items(section)
                )
        return ConfigParams(**config_dict)


params_config: Final = ConfigParser.load_config(os.getenv("CONFIG_PATH", None))
