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

from fastapi import APIRouter, HTTPException, Query, status

from zefir_api.api.crud.zefir_data import method_to_data_category_map
from zefir_api.api.parameters import DataCategory, ScenarioId
from zefir_api.api.payload.zefir_data import (
    ZefirDataResponse,
    ZefirFuelUnitsResponse,
    ZefirTechnologyTranslationResponse,
    ZefirYearsResponse,
)
from zefir_api.api.zefir_engine import ze

zefir_data_router = APIRouter(prefix="/zefir_data")


@zefir_data_router.get("/get_data", response_model=ZefirDataResponse)
def get_zefir_data(
    data_category: DataCategory,
    scenario_id: ScenarioId = Query(ScenarioId.SCENARIO_1),
) -> ZefirDataResponse:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    engine = ze[scenario_id]
    method = method_to_data_category_map[data_category]
    return method(engine)


@zefir_data_router.get("/get_years", response_model=ZefirYearsResponse)
def get_sequence_of_years(scenario_id: ScenarioId) -> ZefirYearsResponse:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    return ZefirYearsResponse.get_years(ze[scenario_id])


@zefir_data_router.get(
    "/get_tags_map", response_model=ZefirTechnologyTranslationResponse
)
def get_translated_tags_map() -> ZefirTechnologyTranslationResponse:
    return ZefirTechnologyTranslationResponse.get_tags()


@zefir_data_router.get("/get_fuel_units", response_model=list[ZefirFuelUnitsResponse])
def get_fuel_units() -> list[ZefirFuelUnitsResponse]:
    return ZefirFuelUnitsResponse.get_units()
