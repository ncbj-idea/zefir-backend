from __future__ import annotations

import pandas as pd
from pydantic import BaseModel


class BuildingGeometry(BaseModel):
    type: str = "Polygon"
    coordinates: list[list[list[float]]]


class BuildingProperty(BaseModel):
    buildingType: str
    heatType: str


class ZefirMapResponse(BaseModel):
    type: str = "Feature"
    id: int
    geometry: BuildingGeometry
    properties: BuildingProperty

    @staticmethod
    def create_from_series(df_row: pd.Series) -> ZefirMapResponse:
        geometry = BuildingGeometry(coordinates=(df_row["coordinates"]))
        properties = BuildingProperty(
            buildingType=df_row["buildingType"], heatType=df_row["heatType"]
        )
        return ZefirMapResponse(
            id=df_row.name, geometry=geometry, properties=properties
        )
