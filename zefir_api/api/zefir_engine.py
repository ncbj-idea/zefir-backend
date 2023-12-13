import os
import re
from pathlib import Path
from typing import Final

from zefir_analytics import ZefirEngine

from zefir_api.api.utils import get_resources

SOURCE_PATH: Final = Path(
    os.getenv(key="SOURCE_PATH", default=get_resources("source_csv"))
)
RESULT_PATH: Final = Path(
    os.getenv(key="RESULT_PATH", default=get_resources("results"))
)
PARAMETER_PATH: Final = Path(
    os.getenv(key="PARAMETER_PATH", default=get_resources("parameters"))
)


def create_zefir_engines() -> dict[int, ZefirEngine]:
    scenarios_folder = SOURCE_PATH / "scenarios"
    return {
        int(id_.group()): ZefirEngine(
            source_path=SOURCE_PATH,
            result_path=RESULT_PATH / scenario_name.name,
            parameter_path=PARAMETER_PATH,
            scenario_name=scenario_name.name,
        )
        for scenario_name in scenarios_folder.iterdir()
        if (id_ := re.search(r"\d+", scenario_name.name)) is not None
    }


ze: Final = create_zefir_engines()
