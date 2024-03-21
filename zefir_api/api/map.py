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


def load_polygon_map_file(filepath: Path) -> gpd.GeoDataFrame:
    df = load_geo_file(filepath)
    df["geometry"] = df["coordinates"].apply(
        lambda x: Polygon([(point[0], point[1]) for point in x[0]])
    )
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:2180")
    return gdf


def load_areas_polygon_maps() -> dict[str, gpd.GeoDataFrame]:
    area_polygon_dict = {}
    for area_dir in params_config.areas_path.iterdir():
        if not area_dir.iterdir():
            continue
        area_name = area_dir.name
        area_polygon_dict[area_name] = load_polygon_map_file(
            params_config.get_polygons_file_path(area_name)
        )
    return area_polygon_dict


def load_areas_points_maps() -> dict[str, pd.DataFrame]:
    area_points_dict = {}
    for area_dir in params_config.areas_path.iterdir():
        if not area_dir.iterdir():
            continue
        area_name = area_dir.name
        area_points_dict[area_name] = load_geo_file(
            params_config.get_points_file_path(area_name)
        )
    return area_points_dict


map_resource: Final = load_areas_polygon_maps()
points_resource: Final = load_areas_points_maps()
