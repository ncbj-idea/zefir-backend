import pandas as pd
from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import (
    flatten_multiindex,
    get_row_amount_of_device_in_agg,
    translate_df_by_map,
)
from zefir_api.api.env_params import TAGS_TO_DROP
from zefir_api.api.mapping import translator
from zefir_api.api.payload.zefir_data import ZefirDataResponse


def _map_name_to_type(ze: ZefirEngine, items: list[str]) -> list[str]:
    mapped_items: list[str] = []
    for item in items:
        if item in ze.network.generators:
            mapped_items.append(ze.network.generators[item].energy_source_type)
        if item in ze.network.storages:
            mapped_items.append(ze.network.storages[item].energy_source_type)
    return mapped_items


def _filter_types_to_not_display_at_installed_power(df: pd.DataFrame) -> pd.DataFrame:
    if translator.translated_tags is None:
        return df
    for drop_tag in TAGS_TO_DROP:
        et_in_tag_names = [
            et_name
            for et_name, tag_name in translator.translated_tags.items()
            if tag_name == drop_tag
        ]
        for et_name in et_in_tag_names:
            if et_name in df.index:
                df = df.drop(et_name)
    return df


def get_installed_power(ze: ZefirEngine) -> ZefirDataResponse:
    power_df = ze.source_params.get_installed_capacity(level="type")
    power_df = flatten_multiindex(df=power_df)
    power_df = _filter_types_to_not_display_at_installed_power(df=power_df)
    power_df = translate_df_by_map(
        df=power_df, mapping_dict=translator.translated_names
    )
    return ZefirDataResponse.from_technology_df(df=power_df)


def get_increasing_amount_of_devices(ze: ZefirEngine) -> ZefirDataResponse:
    fractions = ze.aggregated_consumer_params.get_fractions()
    fractions = {
        name: df.diff().fillna(0.0).clip(lower=0.0) for name, df in fractions.items()
    }
    n_consumers = ze.aggregated_consumer_params.get_n_consumers()
    device_factor = get_row_amount_of_device_in_agg(fractions, n_consumers)
    dfs_power_type_corrections = []
    for df in device_factor.values():
        for lbs_name in df.columns:
            power = ze.lbs_params.get_lbs_capacity(lbs_name)
            power.columns = _map_name_to_type(ze, power.columns)
            a = power.mask(power != 0, df[lbs_name], axis=0)
            dfs_power_type_corrections.append(a)
    device_df = pd.concat(dfs_power_type_corrections, axis=1)
    device_df = device_df.groupby(level=0, axis=1).sum().T
    device_df = translate_df_by_map(
        df=device_df, mapping_dict=translator.translated_names
    )
    return ZefirDataResponse.from_technology_df(df=device_df)
