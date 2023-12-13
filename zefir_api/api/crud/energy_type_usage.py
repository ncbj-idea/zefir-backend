import pandas as pd
from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import flatten_multiindex, get_aggr_by_generator_name
from zefir_api.api.env_params import COLD_US_ET_NAME, EE_US_ET_NAME, HEAT_US_ET_NAME
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
    df = df.rename(
        {
            name: get_aggr_by_generator_name(
                gen_name=name, ze=ze, energy_type=energy_type
            )
            for name in df.index
        }
    )
    if "not_found_energy_type" in df.index:
        df = df.drop(index="not_found_energy_type")
    df = df.groupby(df.index).sum()
    filtered_factor_df = factor_df.loc[factor_df.index.isin(df.index)]
    summed_df = df + filtered_factor_df
    summed_df = _map_agg_name_to_agg_type(summed_df)
    return ZefirDataResponse.from_technology_df(df=summed_df)


def get_ee_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=EE_US_ET_NAME)


def get_heat_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=HEAT_US_ET_NAME)


def get_cold_usage(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_usage(ze=ze, energy_type=COLD_US_ET_NAME)
