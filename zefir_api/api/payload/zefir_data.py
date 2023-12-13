from __future__ import annotations

from typing import Sequence

import pandas as pd
from pydantic import BaseModel
from zefir_analytics import ZefirEngine

from zefir_api.api.mapping import translator


class TechnologyDataResponse(BaseModel):
    technology_name: str
    values: list[float]


class EmissionDataResponse(BaseModel):
    emission_type: str
    data: list[TechnologyDataResponse]


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
        return ZefirYearsResponse(years=list(ze._params["year_sample"].to_numpy()))


class ZefirTechnologyTranslationResponse(BaseModel):
    tags: dict[str, str] | None

    @staticmethod
    def get_tags() -> ZefirTechnologyTranslationResponse:
        return ZefirTechnologyTranslationResponse(tags=translator.translated_tags)
