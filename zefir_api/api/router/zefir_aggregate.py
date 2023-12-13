from fastapi import APIRouter, HTTPException, Query, status

from zefir_api.api.crud.aggregate import get_agg_totals, get_details, get_stacks_info
from zefir_api.api.parameters import AggregateType, ScenarioId
from zefir_api.api.payload.zefir_aggregate import (
    ZefirAggregateDetail,
    ZefirAggregateStacks,
    ZefirAggregateTotals,
)
from zefir_api.api.zefir_engine import ze

zefir_agg_router = APIRouter(prefix="/zefir_aggregate")


@zefir_agg_router.get("/get_totals", response_model=ZefirAggregateTotals)
def get_zefir_agg_totals(
    aggregate_type: AggregateType,
    scenario_id: ScenarioId = Query(ScenarioId.SCENARIO_1),
) -> ZefirAggregateTotals:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    engine = ze[scenario_id]
    return get_agg_totals(engine, aggregate_type)


@zefir_agg_router.get("/get_stacks", response_model=list[ZefirAggregateStacks])
def get_zefir_agg_stacks(
    aggregate_type: AggregateType,
    scenario_id: ScenarioId = Query(ScenarioId.SCENARIO_1),
) -> list[ZefirAggregateStacks]:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    engine = ze[scenario_id]
    return get_stacks_info(engine, aggregate_type)


@zefir_agg_router.get("/details", response_model=list[ZefirAggregateDetail])
def get_zefir_agg_details(
    aggregate_type: AggregateType,
    scenario_id: ScenarioId = Query(ScenarioId.SCENARIO_1),
) -> list[ZefirAggregateDetail]:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    engine = ze[scenario_id]
    return get_details(engine, aggregate_type)
