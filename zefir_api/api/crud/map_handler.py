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

import geopandas as gpd
import pandas as pd
from shapely import geometry
from shapely.geometry import Polygon

from zefir_api.api.payload.zefir_map import (
    ZefirMapBuildingResponse,
    ZefirMapPointResponse,
)


def _found_geometry_in_bbox(
    bbox_polygon: Polygon, gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Finds the indices of geometries within a specified bounding box.

    Parameters:
    - bbox_polygon (Polygon): Shapely Polygon representing the bounding box.
    - gdf (gpd.GeoDataFrame): GeoDataFrame containing geographical resources

    Returns:
    gpd.GeoDataFrame: Filtered gdf containing geometries within the bounding box

    The method performs the following steps:
    1. Determines which geometries from the GeoDataFrame fall within the bounding box.
    2. Returns a GeoDataFrame containing geometries within the specified bounding box.
    """
    return gdf[gdf.geometry.within(bbox_polygon)]


def get_buildings_from_bbox(
    resource_df: gpd.GeoDataFrame, bbox: list[float]
) -> list[ZefirMapBuildingResponse]:
    """
    Retrieves buildings from a DataFrame filtered by a specified bounding box.

    Parameters:
    - resource_df (gpd.GeoDataFrame): GeoDataFrame containing geographical resources.
    - bbox (list): Bounding box coordinates in the form of [min_x, min_y, max_x, max_y].

    Returns:
    list: A list of ZefirMapResponse objects created from the filtered DataFrame.

    The method performs the following steps:
    2. Constructs a bounding box Polygon based on the provided bbox.
    3. Calls the '_found_geometry_in_bbox' method to obtain geometries within the bounding box.
    5. Applies a custom method (ZefirMapResponse.create_from_series) to create a list of ZefirMapResponse objects.
    """
    bbox_polygon = geometry.box(*bbox)
    filtered_df = _found_geometry_in_bbox(bbox_polygon=bbox_polygon, gdf=resource_df)

    return [
        ZefirMapBuildingResponse.create_polygons_from_dict(
            coordinates=data["coordinates"],
            building_type=data["buildingType"],
            heat_type=data["heatType"],
            name=id_,
        )
        for id_, data in filtered_df.to_dict("index").items()
    ]


def get_points(resource_df: pd.DataFrame) -> list[ZefirMapPointResponse]:
    return [
        ZefirMapPointResponse.create_points_from_dict(
            coordinates=data["coordinates"],
            building_type=data["buildingType"],
            heat_type=data["heatType"],
            name=id_,
            boilerEmission=data["boilerEmission"],
            CO2=data["CO2"],
            CO=data["CO"],
            SOX=data["SOX"],
            NOX=data["NOX"],
            Benzoapiren=data["Benzoapiren"],
            PM10=data["PM10"],
            PM25=data["PM25"],
        )
        for id_, data in resource_df.to_dict("index").items()
    ]
