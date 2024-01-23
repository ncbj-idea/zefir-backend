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

import json
from pathlib import Path
from typing import Final

import geopandas as gpd
import pandas as pd
from shapely import Polygon

from zefir_api.api.config import params_config


def load_geo_file(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path, index_col="id")
    df["coordinates"] = df["coordinates"].apply(lambda x: json.loads(x))
    return df


def load_polygon_map_file() -> gpd.GeoDataFrame:
    df = load_geo_file(params_config.polygons_file_path)
    df["geometry"] = df["coordinates"].apply(
        lambda x: Polygon([(point[0], point[1]) for point in x[0]])
    )
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:2180")
    return gdf


map_resource: Final = load_polygon_map_file()
points_resource: Final = load_geo_file(params_config.points_file_path)
