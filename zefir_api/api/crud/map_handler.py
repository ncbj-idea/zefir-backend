import json

import geopandas as gpd
import pandas as pd
from shapely import geometry
from shapely.geometry import Polygon

from zefir_api.api.payload.zefir_map import ZefirMapResponse


def _found_geometry_in_bbox(bbox_polygon: Polygon, df: pd.DataFrame) -> list[int]:
    """
    Finds the indices of geometries within a specified bounding box.

    Parameters:
    - bbox_polygon (Polygon): Shapely Polygon representing the bounding box.
    - df (pd.DataFrame): DataFrame containing geographical resources with a 'coordinates' column.

    Returns:
    list: A list of indices corresponding to the geometries within the specified bounding box.

    The method performs the following steps:
    1. Parses the 'coordinates' column from JSON strings to Python objects.
    2. Generates a 'geometry' column by creating Shapely Polygon objects from the parsed coordinates.
    3. Converts the DataFrame to a GeoDataFrame with the specified coordinate reference system (EPSG:2180).
    4. Determines which geometries from the GeoDataFrame fall within the bounding box.
    5. Returns a list of indices corresponding to the geometries within the specified bounding box.
    """
    df["coordinates"] = df["coordinates"].apply(lambda x: json.loads(x))
    df["geometry"] = df["coordinates"].apply(
        lambda x: Polygon([(point[0], point[1]) for point in x[0]])
    )
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:2180")
    gdf["within_map"] = gdf.geometry.within(bbox_polygon)
    return gdf[gdf["within_map"]].index.to_list()


def get_buildings_from_bbox(
    resource_df: pd.DataFrame, bbox: list[float]
) -> list[ZefirMapResponse]:
    """
    Retrieves buildings from a DataFrame filtered by a specified bounding box.

    Parameters:
    - resource_df (pd.DataFrame): DataFrame containing geographical resources with a 'coordinates' column.
    - bbox (list): Bounding box coordinates in the form of [min_x, min_y, max_x, max_y].

    Returns:
    list: A list of ZefirMapResponse objects created from the filtered DataFrame.

    The method performs the following steps:
    1. Creates a copy of the input DataFrame.
    2. Constructs a bounding box Polygon based on the provided bbox.
    3. Calls the '_found_geometry_in_bbox' method to obtain indices of geometries within the bounding box.
    4. Filters the DataFrame to include only rows with geometries within the specified bounding box.
    5. Applies a custom method (ZefirMapResponse.create_from_series) to create a list of ZefirMapResponse objects.
    """
    df = resource_df.copy()
    bbox_polygon = geometry.box(*bbox)
    found_geom_idx = _found_geometry_in_bbox(bbox_polygon=bbox_polygon, df=df)
    filtered_df = df.loc[found_geom_idx]

    return [
        ZefirMapResponse.create_from_series(row) for _, row in filtered_df.iterrows()
    ]
