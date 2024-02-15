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

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import BaseModel, Field


class PointGeometry(BaseModel):
    type: Literal["Point"] = Field("Point", init=False)
    coordinates: list[float]


PolygonCoordinates: TypeAlias = list[list[list[float]]]


class MultiPolygonGeometry(BaseModel):
    type: Literal["MultiPolygon"] = Field("MultiPolygon", init=False)
    coordinates: list[PolygonCoordinates]


class PolygonGeometry(BaseModel):
    type: Literal["Polygon"] = Field("Polygon", init=False)
    coordinates: PolygonCoordinates


class BuildingProperty(BaseModel):
    buildingType: str
    heatType: str


class PointProperties(BuildingProperty):
    boilerEmission: str
    CO2: float
    CO: float
    SOX: float
    NOX: float
    Benzoapiren: float
    PM10: float
    PM25: float


class ZefirMapBuildingResponse(BaseModel):
    type: str = "Feature"
    id: int
    geometry: PolygonGeometry
    properties: BuildingProperty

    @staticmethod
    def create_polygons_from_dict(
        coordinates: list[list[list[float]]],
        building_type: str,
        heat_type: str,
        name: int,
    ) -> ZefirMapBuildingResponse:
        geometry = PolygonGeometry(coordinates=coordinates)
        properties = BuildingProperty(buildingType=building_type, heatType=heat_type)
        return ZefirMapBuildingResponse(
            id=name, geometry=geometry, properties=properties
        )


class ZefirMapPointResponse(BaseModel):
    type: str = "Feature"
    id: int
    geometry: PointGeometry
    properties: PointProperties

    @staticmethod
    def create_points_from_dict(
        coordinates: list[float],
        building_type: str,
        heat_type: str,
        name: int,
        boilerEmission: str,
        CO2: float,
        CO: float,
        SOX: float,
        NOX: float,
        Benzoapiren: float,
        PM10: float,
        PM25: float,
    ) -> ZefirMapPointResponse:
        geometry = PointGeometry(coordinates=coordinates)
        properties = PointProperties(
            buildingType=building_type,
            heatType=heat_type,
            boilerEmission=boilerEmission,
            CO2=CO2,
            CO=CO,
            SOX=SOX,
            NOX=NOX,
            Benzoapiren=Benzoapiren,
            PM10=PM10,
            PM25=PM25,
        )
        return ZefirMapPointResponse(id=name, geometry=geometry, properties=properties)
