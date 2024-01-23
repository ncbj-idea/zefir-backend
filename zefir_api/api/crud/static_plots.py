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

import pandas as pd

from zefir_api.api.payload.zefir_static import StaticPlotsData, StaticPlotsResponse
from zefir_api.api.static_data import StaticData


def _get_common_sorted_indexes(df_dict: dict[str, pd.DataFrame]) -> list[str]:
    first_df_index = list(df_dict.values())[0].index
    all_same_indexes = all(df.index.equals(first_df_index) for df in df_dict.values())
    if all_same_indexes:
        return first_df_index.tolist()
    else:
        for name, df in df_dict.items():
            df_dict.update({name: df.sort_index()})
        return list(df_dict.values())[0].index.to_list()


def get_static_plots() -> StaticPlotsResponse:
    static_plots_data = StaticData.load_static_plots_data()
    unique_indexes = _get_common_sorted_indexes(static_plots_data)
    for attr_name, df in static_plots_data.items():
        data = [
            StaticPlotsData(name=name, data=data)
            for name, data in df.to_dict(orient="list").items()
        ]
        static_plots_data.update({attr_name: data})
    return StaticPlotsResponse(labels=unique_indexes, **static_plots_data)
