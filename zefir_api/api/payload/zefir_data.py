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

from __future__ import annotations

from typing import Sequence

import pandas as pd
from pydantic import BaseModel
from zefir_analytics import ZefirEngine

from zefir_api.api.static_data import StaticData
from zefir_api.api.translation import translator


class TechnologyDataResponse(BaseModel):
    technology_name: str
    values: list[float]


class EmissionDataResponse(BaseModel):
    emission_type: str
    data: list[TechnologyDataResponse]

    @staticmethod
    def from_emission_dict(
        emission_dict: dict[str, pd.DataFrame]
    ) -> list[EmissionDataResponse]:
        return [
            EmissionDataResponse(
                emission_type=emission_type,
                data=ZefirDataResponse.from_technology_df(df=df).data,
            )
            for emission_type, df in emission_dict.items()
        ]


class EnergyDataResponse(BaseModel):
    fuel_name: str
    usage: list[float]
    power: list[float]


DataResponse = Sequence[
    TechnologyDataResponse | EmissionDataResponse | EnergyDataResponse
]


class ZefirDataResponse(BaseModel):
    years: list[int]
    data: DataResponse

    @staticmethod
    def from_technology_df(df: pd.DataFrame) -> ZefirDataResponse:
        years = [int(year) for year in df.columns.values]
        techs = [
            TechnologyDataResponse(technology_name=name, values=df.loc[name].to_list())
            for name in df.index
        ]
        return ZefirDataResponse(
            years=years,
            data=techs,
        )


class ZefirYearsResponse(BaseModel):
    years: list[int]

    @staticmethod
    def get_years(ze: ZefirEngine) -> ZefirYearsResponse:
        return ZefirYearsResponse(years=ze._year_sample)


class ZefirTechnologyTranslationResponse(BaseModel):
    tags: dict[str, str] | None

    @staticmethod
    def get_tags() -> ZefirTechnologyTranslationResponse:
        return ZefirTechnologyTranslationResponse(
            tags={
                translator.translated_names.get(key, key): value
                for key, value in translator.translated_tags.items()
            }
        )


class ZefirFuelUnitsResponse(BaseModel):
    fuel_name: str
    fuel_unit: str

    @staticmethod
    def get_units() -> list[ZefirFuelUnitsResponse]:
        return [
            ZefirFuelUnitsResponse(
                fuel_name=translator.translated_fuels.get(fuel_name, fuel_name),
                fuel_unit=fuel_unit,
            )
            for fuel_name, fuel_unit in StaticData.load_fuel_units().items()
        ]
