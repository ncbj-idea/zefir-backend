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

from zefir_api.api.config import params_config
from zefir_api.api.crud.utils import (
    flatten_multiindex,
    filter_generators_by_tag,
    translate_df_by_map,
)
from zefir_api.api.payload.zefir_data import ZefirDataResponse
from zefir_api.api.translation import translator


def _get_energy_type_production(ze: ZefirEngine, energy_type: str) -> ZefirDataResponse:
    df = ze.source_params.get_generation_sum(level="type")[[energy_type]].dropna()
    df = flatten_multiindex(df=df)
    thermo_techs = set(
        [g.energy_source_type for g in filter_generators_by_tag(ze=ze, tags=["thermo"])]
    )
    df = df[~df.index.isin(thermo_techs)]
    df = translate_df_by_map(df=df, mapping_dict=translator.translated_names)
    return ZefirDataResponse.from_technology_df(df=df)


def get_ee_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(
        ze=ze, energy_type=params_config.production_ee_name
    )


def get_heat_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(
        ze=ze, energy_type=params_config.production_heat_name
    )


def get_cold_production(ze: ZefirEngine) -> ZefirDataResponse:
    return _get_energy_type_production(
        ze=ze, energy_type=params_config.production_cold_name
    )
