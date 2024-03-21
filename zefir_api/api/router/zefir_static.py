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

from fastapi import APIRouter, HTTPException, status

from zefir_api.api.crud.scenario_description import generate_scenarios_description
from zefir_api.api.crud.static_aggr_data import get_aggr_static_data
from zefir_api.api.crud.static_plots import get_static_plots
from zefir_api.api.payload.zefir_static import (
    StaticAggrDataResponse,
    StaticPlotsResponse,
    StaticScenarioDescriptionResponse,
)
from zefir_api.api.zefir_engine import area_scenario_mapping

zefir_static_router = APIRouter(prefix="/zefir_static")


@zefir_static_router.get("/get_plots", response_model=StaticPlotsResponse)
def get_plots(area_id: int = 0) -> StaticPlotsResponse:
    area = area_scenario_mapping.get(area_id)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Area ID {area_id} not found",
        )
    return get_static_plots(area.name)


@zefir_static_router.get("/get_aggr_data", response_model=list[StaticAggrDataResponse])
def get_aggr_data(area_id: int = 0) -> list[StaticAggrDataResponse]:
    area = area_scenario_mapping.get(area_id)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Area ID {area_id} not found",
        )
    return get_aggr_static_data(area.name)


@zefir_static_router.get(
    "/get_scenario_description", response_model=list[StaticScenarioDescriptionResponse]
)
def get_scenario_description(
    area_id: int = 0,
) -> list[StaticScenarioDescriptionResponse]:
    area = area_scenario_mapping.get(area_id)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Area ID {area_id} not found",
        )
    return generate_scenarios_description(area)
