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

import pandas as pd
from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import (
    flatten_multiindex,
    filter_generators_by_tag,
    translate_df_by_map,
)
from zefir_api.api.payload.zefir_data import ZefirDataResponse
from zefir_api.api.translation import translator
from zefir_api.api.transport_loader import transport_holder
from zefir_api.api.zefir_engine import get_scenario_id


def _calculate_ets_emission_costs(
    ze: ZefirEngine, emissions_df: pd.DataFrame, years: list[int]
) -> dict[str, pd.DataFrame]:
    emissions_dict = {
        emission_name: flatten_multiindex(emissions_df[[emission_name]])
        for emission_name in emissions_df.columns
    }
    ets_fee_dict: dict[str, dict] = defaultdict(dict)
    for ets in ze.network.emission_fees.values():
        ets_fee_dict[ets.emission_type][ets.name] = ets.price.loc[years].T
    if not ets_fee_dict:
        return {}
    ets_fee_dict = dict(ets_fee_dict)
    for et, df in emissions_dict.items():
        if et in ets_fee_dict:
            emission_fees_per_et = set(ets_fee_dict[et].keys())
            for gen_name in df.index:
                gen_ef = ze.network.generators[gen_name].emission_fee
                common_gen_ef = emission_fees_per_et.intersection(gen_ef)
                if not gen_ef or not common_gen_ef:
                    df = df.drop(gen_name)
                else:
                    ets_df = ets_fee_dict[et][common_gen_ef.pop()].to_list()
                    df.loc[[gen_name]] = df.loc[[gen_name]].mul(ets_df)
            emissions_dict[et] = df
    return emissions_dict


def _get_cost_type(
    ze: ZefirEngine, cost_type: str, thermo_capex: bool = False
) -> ZefirDataResponse:
    df = ze.source_params.get_capex_opex(level="type")[[cost_type]].dropna()
    df = flatten_multiindex(df=df)
    if cost_type == "capex":
        capex_transport_df = transport_holder.get_capex(
            get_scenario_id(ze.scenario_name)
        )
        if thermo_capex:
            df = df[df.index.isin(filter_generators_by_tag(ze=ze, tags=["thermo"]))]
        df = pd.concat([df, capex_transport_df])
    return ZefirDataResponse.from_technology_df(df)


def _calculate_var_cost(ze: ZefirEngine) -> pd.DataFrame:
    fuel_usage = ze.source_params.get_fuel_usage(level="type")
    fuel_cost = ze.source_params.get_fuel_cost(level="type")
    df_var_cost = pd.DataFrame({"var_cost": fuel_usage.multiply(fuel_cost).sum(axis=1)})
    return flatten_multiindex(df=df_var_cost)


def _calculate_ets_fee(ze: ZefirEngine) -> pd.DataFrame:
    # element because mapping gen -> ets
    emissions_df = ze.source_params.get_emission(level="element")
    years = emissions_df.index.get_level_values(1).unique().to_list()
    emissions_dict = _calculate_ets_emission_costs(
        ze=ze, emissions_df=emissions_df, years=years
    )
    if not emissions_dict:
        return pd.DataFrame(columns=years)
    result_df = pd.concat(emissions_dict.values(), axis=0)
    result_df = result_df.groupby(result_df.index).sum()
    gen_to_gen_type_map = {
        gen: ze.network.generators[gen].energy_source_type
        for gen in result_df.index.to_list()
    }
    result_df.index = result_df.index.map(gen_to_gen_type_map)
    return result_df.groupby(result_df.index).sum()


def get_capex(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_cost_type(ze=ze, cost_type="capex")


def get_thermo_capex(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_cost_type(ze=ze, cost_type="capex", thermo_capex=True)


def get_opex(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_cost_type(ze=ze, cost_type="opex")


def get_var_cost(ze: ZefirEngine) -> ZefirDataResponse:
    df = _calculate_var_cost(ze)
    df = translate_df_by_map(df=df, mapping_dict=translator.translated_names)
    return ZefirDataResponse.from_technology_df(df=df)


def get_ets(ze: ZefirEngine) -> ZefirDataResponse:
    df = _calculate_ets_fee(ze)
    df = translate_df_by_map(df=df, mapping_dict=translator.translated_names)
    return ZefirDataResponse.from_technology_df(df=df)


def get_total_costs(ze: ZefirEngine) -> ZefirDataResponse:
    capex_opex = ze.source_params.get_capex_opex(level="type")
    capex, opex = capex_opex[["capex"]], capex_opex[["opex"]]
    capex = flatten_multiindex(capex.dropna()).sum()
    opex = flatten_multiindex(opex.dropna()).sum()
    var_cost = _calculate_var_cost(ze).sum()
    ets = _calculate_ets_fee(ze).sum()
    df = pd.concat(
        [capex, opex, var_cost, ets], axis=1, keys=["capex", "opex", "var_cost", "ets"]
    ).T
    return ZefirDataResponse.from_technology_df(df=df)
