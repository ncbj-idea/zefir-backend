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
