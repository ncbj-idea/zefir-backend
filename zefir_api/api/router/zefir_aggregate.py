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

from zefir_api.api.crud.aggregate import get_agg_totals, get_details, get_stacks_info
from zefir_api.api.parameters import AggregateType
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
    scenario_id: int = Query(0),
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
    scenario_id: int = Query(0),
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
    scenario_id: int = Query(0),
) -> list[ZefirAggregateDetail]:
    if scenario_id not in ze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario_id {scenario_id} not found",
        )
    engine = ze[scenario_id]
    return get_details(engine, aggregate_type)
