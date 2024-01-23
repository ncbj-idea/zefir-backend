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

from fastapi import APIRouter, Query

from zefir_api.api.crud.map_handler import get_buildings_from_bbox, get_points
from zefir_api.api.map import map_resource, points_resource
from zefir_api.api.payload.zefir_map import (
    ZefirMapBuildingResponse,
    ZefirMapPointResponse,
)

zefir_map_router = APIRouter(prefix="/zefir_map")


@zefir_map_router.get("/get_buildings", response_model=list[ZefirMapBuildingResponse])
def get_filtered_geometries(
    bbox: list[float] = Query(..., description="Bounding box as a list of coordinates")
) -> list[ZefirMapBuildingResponse]:
    return get_buildings_from_bbox(resource_df=map_resource, bbox=bbox)


@zefir_map_router.get("/get_points", response_model=list[ZefirMapPointResponse])
def get_map_points() -> list[ZefirMapPointResponse]:
    return get_points(resource_df=points_resource)
