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
    fuel_units_path: Path = get_resources("fuel_units.json")
    areas_path: Path = get_resources("areas")
    areas_mapping_filepath: Path = get_resources("area_scenario_mapping.json")
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

    def get_source_path(self, area: str) -> Path:
        return self.areas_path / area / "source_csv"

    def get_result_path(self, area: str) -> Path:
        return self.areas_path / area / "results"

    def get_config_path(self, area: str, scenario_name: str) -> Path:
        return self.areas_path / area / "configs" / f"{scenario_name}.ini"

    def get_year_sample_path(self, area: str) -> Path:
        return self.areas_path / area / "parameters" / "year_sample.csv"

    def get_hour_sample_path(self, area: str) -> Path:
        return self.areas_path / area / "parameters" / "hour_sample.csv"

    def get_discount_rate_path(self, area: str) -> Path:
        return self.areas_path / area / "parameters" / "discount_rate.csv"

    def get_polygons_file_path(self, area: str) -> Path:
        return self.areas_path / area / "map/polygonsFeatures.csv"

    def get_points_file_path(self, area: str) -> Path:
        return self.areas_path / area / "map/pointsFeatures.csv"

    def get_plots_path(self, area: str) -> Path:
        return self.areas_path / area / "static_data/static_plots"

    def get_aggregate_data_path(self, area: str) -> Path:
        return self.areas_path / area / "static_data/static_aggr_data"

    def get_transport_path(self, area: str) -> Path:
        return self.areas_path / area / "transport"


class ConfigParser:
    @staticmethod
    def load_config(config_file_path: str | None = None) -> ConfigParams:
        if config_file_path is None:
            return ConfigParams()
        config = configparser.ConfigParser()
        config.read(Path(config_file_path))
        config_dict: dict = {}
        for section in ["names", "paths", "tags", "optimization"]:
            if config.has_section(section):
                config_dict.update(
                    (
                        key,
                        (
                            Path(value)
                            if section == "paths"
                            else value.split("-") if section == "tags" else value
                        ),
                    )
                    for key, value in config.items(section)
                )
        return ConfigParams(**config_dict)


params_config: Final[ConfigParams] = ConfigParser.load_config(
    os.getenv("CONFIG_PATH", None)
)
