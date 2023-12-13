from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import flatten_multiindex, translate_df_by_map
from zefir_api.api.env_params import (
    COLD_PROD_ET_NAME,
    EE_PROD_ET_NAME,
    HEAT_PROD_ET_NAME,
)
from zefir_api.api.mapping import translator
from zefir_api.api.payload.zefir_data import ZefirDataResponse


def _get_energy_type_production(ze: ZefirEngine, energy_type: str) -> ZefirDataResponse:
    df = ze.source_params.get_generation_sum(level="type")[[energy_type]].dropna()
    df = flatten_multiindex(df=df)
    df = translate_df_by_map(df=df, mapping_dict=translator.translated_names)
    return ZefirDataResponse.from_technology_df(df=df)


def get_ee_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(ze=ze, energy_type=EE_PROD_ET_NAME)


def get_heat_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(ze=ze, energy_type=HEAT_PROD_ET_NAME)


def get_cold_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(ze=ze, energy_type=COLD_PROD_ET_NAME)
