import os
from typing import Final

TAGS_TO_DROP: Final = os.getenv("DROP_LIST_TAGS", "KSE-KSE_CONN-HD_CONN").split("-")
EE_PROD_ET_NAME: Final = os.getenv("EE_PRODUCTION_ENERGY_TYPE_NAME", "EE")
HEAT_PROD_ET_NAME: Final = os.getenv("HEAT_PRODUCTION_ENERGY_TYPE_NAME", "HEAT")
COLD_PROD_ET_NAME: Final = os.getenv("COLD_PRODUCTION_ENERGY_TYPE_NAME", "COLD")
EE_US_ET_NAME: Final = os.getenv("EE_USAGE_ENERGY_TYPE_NAME", "EE")
HEAT_US_ET_NAME: Final = os.getenv("HEAT_USAGE_ENERGY_TYPE_NAME", "HEAT")
COLD_US_ET_NAME: Final = os.getenv("COLD_USAGE_ENERGY_TYPE_NAME", "COLD")