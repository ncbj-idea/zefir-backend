from fastapi import APIRouter, HTTPException, Query, status

from zefir_api.api.crud.zefir_data import method_to_data_category_map
from zefir_api.api.parameters import DataCategory, ScenarioId
from zefir_api.api.payload.zefir_data import (
    ZefirDataResponse,
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
