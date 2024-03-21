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
from typing import Final

import pandas as pd

from zefir_api.api.config import params_config
from zefir_api.api.zefir_engine import area_scenario_mapping


class TransportLoader:
    @staticmethod
    def load_data(
        emission_prefix: str = "emission_",
        capex_name: str = "capex",
    ) -> tuple[dict[int, pd.DataFrame], dict[int, dict[str, pd.DataFrame]]]:
        emission_dict: dict[int, dict[str, pd.DataFrame]] = defaultdict(dict)
        capex_dict: dict[int, pd.DataFrame] = {}
        for area in area_scenario_mapping.values():
            area_transport_path = params_config.get_transport_path(area.name)
            for scenario in area.scenarios:
                for file_path in (area_transport_path / scenario.name).iterdir():
                    file_name = file_path.stem
                    if emission_prefix in file_name:
                        emission_type = file_name.replace(emission_prefix, "")
                        df = pd.read_csv(file_path, index_col="Year").T
                        df.columns = df.columns.astype(int)
                        emission_dict[scenario.id][emission_type] = df
                    elif file_name == capex_name:
                        df = pd.read_csv(file_path, index_col="Year").T
                        df.columns = df.columns.astype(int)
                        capex_dict[scenario.id] = df

        return capex_dict, emission_dict


class TransportDataHolder:
    def __init__(self) -> None:
        self._capex, self._emissions = TransportLoader.load_data()

    @property
    def capex(self) -> dict[int, pd.DataFrame]:
        return self._capex

    @property
    def emissions(self) -> dict[int, dict[str, pd.DataFrame]]:
        return self._emissions

    def get_capex(self, scenario_id: int) -> pd.DataFrame:
        if scenario_id not in self._capex:
            raise KeyError(f"{scenario_id} not found in loaded resources")
        return self._capex[scenario_id]

    def get_transport_emissions(self, scenario_id: int) -> dict[str, pd.DataFrame]:
        if scenario_id not in self._emissions:
            raise KeyError(f"{scenario_id} not found in loaded resources")
        return self._emissions[scenario_id]


transport_holder: Final = TransportDataHolder()
