from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import flatten_multiindex, translate_df_by_map
from zefir_api.api.mapping import translator
from zefir_api.api.payload.zefir_data import (
    EmissionDataResponse,
    EnergyDataResponse,
    ZefirDataResponse,
)


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
    if "KSE_VIRTUAL_FUEL" in fuel_usage_df.index:
        fuel_usage_df = fuel_usage_df.drop("KSE_VIRTUAL_FUEL")
    years = fuel_usage_df.index.get_level_values(1).unique().astype(int).to_list()
    fuel_usage_dict = {
        emission_name: flatten_multiindex(fuel_usage_df[[emission_name]])
        .sum()
        .to_list()
        for emission_name in fuel_usage_df.columns
    }
    techs = [
        EnergyDataResponse(
            fuel_name=translator.translated_fuels.get(fuel_name, fuel_name),
            usage=values,
            power=[
                value * ze.network.fuels[fuel_name].energy_per_unit for value in values
            ],
        )
        for fuel_name, values in fuel_usage_dict.items()
    ]
    return ZefirDataResponse(years=years, data=techs)
