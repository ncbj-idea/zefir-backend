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

from dataclasses import dataclass
from enum import Enum, StrEnum, auto, unique


@unique
class DataCategory(StrEnum):
    INSTALLED_POWER = auto()
    EE_PRODUCTION = auto()
    HEAT_PRODUCTION = auto()
    COLD_PRODUCTION = auto()
    EE_USAGE = auto()
    HEAT_USAGE = auto()
    COLD_USAGE = auto()
    AMOUNT_OF_DEVICES = auto()
    EMISSIONS = auto()
    TRANSPORT_EMISSIONS = auto()
    FUEL_USAGE = auto()
    CAPEX = auto()
    THERMO_CAPEX = auto()
    OPEX = auto()
    VAR_COST = auto()
    ETS = auto()
    TOTAL_COSTS = auto()


@unique
class AggregateType(StrEnum):
    SINGLE_FAMILY = auto()
    MULTI_FAMILY = auto()
    SHOP_SERVICE = auto()
    OFFICE = auto()
    OTHER = auto()


@unique
class ConsumptionType(Enum):
    very_high_consumption = "_EF"
    high_consumption = "_D"
    average_consumption = "_C"
    low_consumption = "_AB"


@unique
class StaticPlotsFileNames(StrEnum):
    EE_USAGE = auto()
    GAS_ENABLE = auto()
    HEAT_ENABLE = auto()
    HEAT_USAGE = auto()
    HEATED_AREA = auto()


@dataclass(frozen=True)
class Scenario:
    id: int
    name: str
    description: str


@dataclass(frozen=True)
class Area:
    id: int
    name: str
    scenarios: tuple[Scenario, ...]
