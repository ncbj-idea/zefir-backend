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
import numpy as np
import pandas as pd
from zefir_analytics import ZefirEngine

from zefir_api.api.config import params_config
from zefir_api.api.crud.utils import (
    flatten_multiindex,
    get_mapped_generator_to_aggr,
    filter_generators_by_tag,
)
from zefir_api.api.parameters import AggregateType
from zefir_api.api.payload.zefir_data import ZefirDataResponse


def _get_aggregate_consumer_factor(
    ze: ZefirEngine, years: list[int], energy_type: str
) -> pd.DataFrame:
    factor_df = pd.DataFrame()
    network = ze.network
    for aggr in network.aggregated_consumers.values():
        year_usage = aggr.yearly_energy_usage[energy_type].loc[years]
        n_cons = aggr.n_consumers.loc[years]
        factor_df[aggr.name] = year_usage * n_cons
    factor_df = factor_df.T
    factor_df.columns = [col for col in factor_df.columns]
    return factor_df


def _map_agg_name_to_agg_type(df: pd.DataFrame) -> pd.DataFrame:
    aggregate_map_dict = {
        index: aggregate_type.value.upper()
        for index in df.index
        for aggregate_type in AggregateType
        if aggregate_type.name in index
    }
    df.index = df.index.map(aggregate_map_dict)
    return df.groupby(df.index).sum()


def _get_energy_type_usage(ze: ZefirEngine, energy_type: str) -> ZefirDataResponse:
    # element because we mapping gen -> aggr
    df = ze.source_params.get_generation_demand(level="element")
    factor_df = _get_aggregate_consumer_factor(
        ze=ze,
        years=df.index.get_level_values("Year").astype(int).unique().to_list(),
        energy_type=energy_type,
    )
    if energy_type not in df.columns:
        factor_df = _map_agg_name_to_agg_type(factor_df)
        return ZefirDataResponse.from_technology_df(df=factor_df)
    df = flatten_multiindex(df=df)
    df = get_mapped_generator_to_aggr(df=df, ze=ze, energy_type=energy_type)
    filtered_factor_df = factor_df.loc[factor_df.index.isin(df.index)]
    series_list = []
    for t in filter_generators_by_tag(ze=ze, tags=["thermo"]):
        series = ze.result_dict["generators_results"]["generation"][t.name].sum()
        series.name = t.name
        series_list.append(series)
    df_tech = pd.concat(series_list, axis=1).T
    df_tech.columns = df_tech.columns.astype(np.integer)
    df_tech = get_mapped_generator_to_aggr(df=df_tech, ze=ze, energy_type=energy_type)
    summed_df = df + filtered_factor_df - df_tech
    summed_df = _map_agg_name_to_agg_type(summed_df)
    return ZefirDataResponse.from_technology_df(df=summed_df)


def get_ee_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=params_config.usage_ee_name)


def get_heat_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=params_config.usage_heat_name)


def get_cold_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=params_config.usage_cold_name)
