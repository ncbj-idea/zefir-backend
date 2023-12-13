from enum import Enum, IntEnum, StrEnum, auto, unique


@unique
class ScenarioId(IntEnum):
    SCENARIO_1 = auto()
    SCENARIO_2 = auto()
    SCENARIO_3 = auto()
    SCENARIO_4 = auto()
    SCENARIO_5 = auto()
    SCENARIO_6 = auto()
    SCENARIO_7 = auto()
    SCENARIO_8 = auto()
    SCENARIO_9 = auto()
    SCENARIO_10 = auto()


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
    FUEL_USAGE = auto()
    CAPEX = auto()
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
