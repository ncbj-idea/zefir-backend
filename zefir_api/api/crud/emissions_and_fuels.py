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

from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import flatten_multiindex, translate_df_by_map
from zefir_api.api.payload.zefir_data import (
    EmissionDataResponse,
    EnergyDataResponse,
    ZefirDataResponse,
    ZefirYearsResponse,
)
from zefir_api.api.translation import translator
from zefir_api.api.transport_loader import transport_holder


def get_emissions(ze: ZefirEngine) -> ZefirDataResponse:
    emissions_df = ze.source_params.get_emission(level="type")
    fuel_names = {
        type_name: ze.network.generator_types[type_name].fuel
        for type_name in emissions_df.index.get_level_values(0).unique()
    }
    emissions_df = (
        emissions_df.rename(fuel_names).groupby(level=emissions_df.index.names).sum()
    )
    years = emissions_df.index.get_level_values(1).unique().to_list()
    emissions_dict = {
        emission_name: flatten_multiindex(emissions_df[[emission_name]])
        for emission_name in emissions_df.columns
    }
    emissions = [
        EmissionDataResponse(
            emission_type=emission_type,
            data=ZefirDataResponse.from_technology_df(
                translate_df_by_map(df=df, mapping_dict=translator.translated_fuels)
            ).data,
        )
        for emission_type, df in emissions_dict.items()
    ]
    return ZefirDataResponse(years=years, data=emissions)


def get_fuel_usage(ze: ZefirEngine) -> ZefirDataResponse:
    fuel_usage_df = ze.source_params.get_fuel_usage(level="type")
    # it's hardcode for a deadline mode but after that we should handle it better
    if "KSE_VIRTUAL_FUEL" in fuel_usage_df.columns:
        fuel_usage_df = fuel_usage_df.drop("KSE_VIRTUAL_FUEL", axis=1)
    years = fuel_usage_df.index.get_level_values(1).unique().astype(int).to_list()
    fuel_usage_df.columns = fuel_usage_df.columns.map(translator.translated_fuels)
    fuel_usage_df = fuel_usage_df.groupby(fuel_usage_df.columns, axis=1).sum()
    fuel_usage_dict = {
        emission_name: flatten_multiindex(fuel_usage_df[[emission_name]])
        .sum()
        .to_list()
        for emission_name in fuel_usage_df.columns
    }
    reverse_translation = {v: k for k, v in translator.translated_fuels.items()}
    techs = [
        EnergyDataResponse(
            fuel_name=fuel_name,
            usage=values,
            power=[
                value
                * ze.network.fuels[
                    reverse_translation.get(fuel_name, fuel_name)
                ].energy_per_unit
                for value in values
            ],
        )
        for fuel_name, values in fuel_usage_dict.items()
    ]
    return ZefirDataResponse(years=years, data=techs)


def get_transport_emissions(ze: ZefirEngine) -> ZefirDataResponse:
    years = ZefirYearsResponse.get_years(ze).years
    emission_dict = transport_holder.get_transport_emissions(
        scenario_name=ze._scenario_name
    )
    emissions = EmissionDataResponse.from_emission_dict(emission_dict=emission_dict)
    return ZefirDataResponse(years=years, data=emissions)
