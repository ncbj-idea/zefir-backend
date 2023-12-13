import os
from pathlib import Path
from typing import Final

import pandas as pd

_api_version: Final[str] = "1"
_api_prefix: Final[str] = f"/api/v{_api_version}"

RESOURCES_PATH: Final = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "simple-data-case",
)


def get_api_prefix() -> str:
    return _api_prefix


def get_api_version() -> str:
    return _api_version


def get_resources(x: str | Path) -> Path:
    return Path(os.path.join(RESOURCES_PATH, x))


def load_map_file() -> pd.DataFrame | str:
    MAP_FILE_PATH: Final = os.getenv(
        "MAP_FILE_PATH", get_resources("map/polygonsFeatures.csv")
    )
    if not Path(MAP_FILE_PATH).exists():
        raise FileNotFoundError(
            f"Cannot find resources file under the path: {Path(MAP_FILE_PATH)}"
        )
    return pd.read_csv(Path(MAP_FILE_PATH), index_col="id")


map_resource: Final = load_map_file()
[
    [
        [21.043024529443795, 52.31246629855156],
        [21.04309572538, 52.312479458095474],
        [21.043108631215343, 52.312453780020014],
        [21.043125513700012, 52.31245708575527],
        [21.04316259561798, 52.312382778199975],
        [21.043074513230536, 52.31236622307965],
        [21.043062999277478, 52.312390258037674],
        [21.043045048952116, 52.31238607130763],
        [21.04302099690247, 52.31243739699859],
        [21.043037586095934, 52.312440707820855],
        [21.043024529443795, 52.31246629855156],
    ]
]
