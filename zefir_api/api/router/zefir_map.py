from fastapi import APIRouter, Query

from zefir_api.api.crud.map_handler import get_buildings_from_bbox
from zefir_api.api.payload.zefir_map import ZefirMapResponse
from zefir_api.api.utils import map_resource

zefir_map_router = APIRouter(prefix="/zefir_map")


@zefir_map_router.get("/get_buildings", response_model=list[ZefirMapResponse])
async def get_filtered_geometries(
    bbox: list[float] = Query(..., description="Bounding box as a list of coordinates")
) -> list[ZefirMapResponse]:
    return get_buildings_from_bbox(resource_df=map_resource, bbox=bbox)
