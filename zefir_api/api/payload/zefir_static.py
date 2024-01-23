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

from datetime import datetime

from pydantic import BaseModel


class StaticPlotsData(BaseModel):
    name: str
    data: list[float]


class StaticPlotsResponse(BaseModel):
    labels: list[str]
    heat_usage: list[StaticPlotsData]
    heated_area: list[StaticPlotsData]
    gas_enable: list[StaticPlotsData]
    heat_enable: list[StaticPlotsData]
    ee_usage: list[StaticPlotsData]


class StaticConsumptionData(BaseModel):
    heat_usage: float
    ee_usage: float
    cold_usage: float


class StaticAggrDetails(BaseModel):
    consumption_type: str
    data: StaticConsumptionData

    @staticmethod
    def create_from_dict(
        consumption_type: str, data_dict: dict[str, float]
    ) -> StaticAggrDetails:
        return StaticAggrDetails(
            consumption_type=consumption_type, data=StaticConsumptionData(**data_dict)
        )


class StaticAggrDataResponse(BaseModel):
    aggr_type: str
    data: list[StaticAggrDetails]


class StaticScenarioDescriptionResponse(BaseModel):
    id: int
    name: str
    total_cost: float
    total_capex: float
    total_opex: float
    total_varcost: float
    total_emission_CO2: float
    date: datetime
    description: str
    analyze_time: int
    analyze_step: int
