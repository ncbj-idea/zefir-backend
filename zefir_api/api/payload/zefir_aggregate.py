from __future__ import annotations

from pydantic import BaseModel


class ZefirAggregateTotals(BaseModel):
    total_usable_area: list[float]
    total_amount_of_buildings: list[int]


class ZefirAggregateStacks(BaseModel):
    stack_name: str
    techs: list[str]


class AreaData(BaseModel):
    stack_name: str
    values: list[float]


class UsagePerBuildingData(BaseModel):
    energy_type: str
    values: list[float]


class ZefirAggregateDetail(BaseModel):
    name: str
    area: list[AreaData]
    energy_per_building: list[UsagePerBuildingData]
    agg_area: list[float]
    agg_amount_of_building: list[int]
