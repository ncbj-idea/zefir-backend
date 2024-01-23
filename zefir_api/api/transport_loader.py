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

from collections import defaultdict
from pathlib import Path
from typing import Final

import pandas as pd

from zefir_api.api.config import params_config


class TransportLoader:
    @staticmethod
    def load_data(
        resources_path: Path,
        emission_prefix: str = "emission_",
        capex_name: str = "capex",
    ) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, pd.DataFrame]]]:
        emission_dict: dict[str, dict[str, pd.DataFrame]] = defaultdict(dict)
        capex_dict: dict[str, pd.DataFrame] = {}
        for scenario_folder in resources_path.iterdir():
            scenario_name = scenario_folder.name
            for file_path in scenario_folder.iterdir():
                file_name = file_path.stem
                if emission_prefix in file_name:
                    emission_type = file_name.replace(emission_prefix, "")
                    df = pd.read_csv(file_path, index_col="Year").T
                    df.columns = df.columns.astype(int)
                    emission_dict[scenario_name][emission_type] = df
                elif file_name == capex_name:
                    df = pd.read_csv(file_path, index_col="Year").T
                    df.columns = df.columns.astype(int)
                    capex_dict[scenario_name] = df
        return capex_dict, emission_dict


class TransportDataHolder:
    def __init__(self, resources_path: str | Path) -> None:
        self._capex, self._emissions = TransportLoader.load_data(
            resources_path=Path(resources_path)
        )

    @property
    def capex(self) -> dict[str, pd.DataFrame]:
        return self._capex

    @property
    def emissions(self) -> dict[str, dict[str, pd.DataFrame]]:
        return self._emissions

    def get_capex(self, scenario_name: str) -> pd.DataFrame:
        if scenario_name not in self._capex:
            raise KeyError(f"{scenario_name} not found in loaded resources")
        return self._capex[scenario_name]

    def get_transport_emissions(self, scenario_name: str) -> dict[str, pd.DataFrame]:
        if scenario_name not in self._emissions:
            raise KeyError(f"{scenario_name} not found in loaded resources")
        return self._emissions[scenario_name]


transport_holder: Final = TransportDataHolder(params_config.transport_path)
