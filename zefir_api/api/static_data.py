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

from pathlib import Path
from typing import Iterable

import pandas as pd

from zefir_api.api.config import params_config
from zefir_api.api.loader import JsonLoader
from zefir_api.api.parameters import AggregateType, StaticPlotsFileNames


class StaticDataError(Exception):
    ...


class StaticData(JsonLoader):
    @staticmethod
    def load_fuel_units() -> dict[str, str]:
        return StaticData._load_json(json_path=params_config.fuel_units_path)

    @staticmethod
    def load_csv_to_dict(
        path: Path, index_col: str, enum: Iterable
    ) -> dict[str, pd.DataFrame]:
        data_dict: dict[str, pd.DataFrame] = {}
        for csv_name in enum:
            csv_path = path / f"{csv_name}.csv"
            data_dict[f"{csv_name}"] = pd.read_csv(csv_path, index_col=index_col)
        return data_dict

    @staticmethod
    def load_static_plots_data() -> dict[str, pd.DataFrame]:
        return StaticData.load_csv_to_dict(
            path=params_config.plots_path,
            index_col="name",
            enum=StaticPlotsFileNames,
        )

    @staticmethod
    def load_static_aggr_data() -> dict[str, pd.DataFrame]:
        return StaticData.load_csv_to_dict(
            path=params_config.aggregate_data_path,
            index_col="aggr_type",
            enum=AggregateType,
        )

    @staticmethod
    def load_scenarios_description(scenario_name: str) -> str:
        return StaticData._load_json(
            json_path=params_config.scenario_description_path,
        )[scenario_name]
