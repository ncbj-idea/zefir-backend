# NCBR_backend
# Copyright (C) 2024 Narodowe Centrum Badań Jądrowych
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

from collections.abc import Sequence

from fastapi import APIRouter, HTTPException
from starlette import status

from zefir_api.api.parameters import Area, Scenario
from zefir_api.api.zefir_engine import area_scenario_mapping

areas_router = APIRouter(prefix="/areas")


@areas_router.get("/")
def get_areas() -> list[Area]:
    return list(area_scenario_mapping.values())


@areas_router.get("/{area_id}")
def get_scenarios_for_area(area_id: int) -> Sequence[Scenario]:
    area = area_scenario_mapping.get(area_id)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Area ID {area_id} not found",
        )

    return area.scenarios
