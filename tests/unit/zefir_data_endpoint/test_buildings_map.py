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

import pytest
from fastapi.testclient import TestClient
from starlette import status

from zefir_api.api.payload.zefir_map import PolygonCoordinates


@pytest.mark.parametrize(
    "polygon_coordinates, expected_ids",
    (
        pytest.param(
            (
                (
                    (21.008532090428147, 52.230679139264296),
                    (21.008532090428147, 52.23271196434463),
                    (21.003805955045422, 52.23271196434463),
                    (21.003805955045422, 52.230679139264296),
                    (21.008532090428147, 52.230679139264296),
                ),
            ),
            (5942,),
            id="1 building",
        ),
        pytest.param(
            (
                (
                    (20.875032709421458, 52.18175410575409),
                    (20.875032709421458, 52.1843402389807),
                    (20.869023197591606, 52.1843402389807),
                    (20.869023197591606, 52.18175410575409),
                    (20.875032709421458, 52.18175410575409),
                ),
            ),
            (
                471,
                803,
                823,
                2725,
                4367,
                5411,
                6348,
                7222,
                7223,
                8407,
                18900,
                19628,
                21912,
                24470,
                27510,
                34242,
                35894,
                36010,
                36408,
                36410,
                41735,
                44164,
                45428,
                50771,
                52057,
                52934,
                58689,
                59007,
                59382,
                60789,
                61575,
                61840,
                64330,
                66181,
                71334,
                71581,
                73171,
                73243,
                75096,
                75470,
                78456,
            ),
            id="40 buildings",
        ),
    ),
)
def test_zefir_map_filter_by_polygon(
    client: TestClient, polygon_coordinates: PolygonCoordinates, expected_ids: list[int]
) -> None:
    response = client.post(
        "/zefir_map/polygon_buildings",
        json={
            "coordinates": polygon_coordinates,
            "type": "Polygon",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(expected_ids)
    list_of_ids = [obj["id"] for obj in data]
    assert sorted(list_of_ids) == sorted(expected_ids)


def test_zefir_map_filter_handle_huge_amount(client: TestClient) -> None:
    coordinates = (
        (
            (21.21099067118059, 52.18071951587461),
            (21.21099067118059, 52.245914444148504),
            (21.059447057006928, 52.245914444148504),
            (21.059447057006928, 52.18071951587461),
            (21.21099067118059, 52.18071951587461),
        ),
    )
    response = client.post(
        "/zefir_map/polygon_buildings",
        json={
            "coordinates": coordinates,
            "type": "Polygon",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 18504


def test_zefir_map_multipolygon(client: TestClient) -> None:
    coordinates = (
        (
            (
                (20.99859322904291, 52.23129969461175),
                (21.004797362980923, 52.23129969461175),
                (21.004797362980923, 52.233722136915475),
                (21.01144376621025, 52.233722136915475),
                (21.01144376621025, 52.23484908109384),
                (20.99859322904291, 52.23484908109384),
                (20.99859322904291, 52.23129969461175),
            ),
        ),
        (
            (
                (21.0152381806071, 52.22465802347625),
                (21.024108641570194, 52.22465802347625),
                (21.024108641570194, 52.22859092802119),
                (21.02106453371215, 52.22859092802119),
                (21.02106453371215, 52.2271567155791),
                (21.0152381806071, 52.2271567155791),
                (21.0152381806071, 52.22465802347625),
            ),
        ),
    )
    response = client.post(
        "/zefir_map/multipolygon_buildings",
        json={
            "coordinates": coordinates,
            "type": "MultiPolygon",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 95


@pytest.mark.parametrize(
    "endpoint, type_, expected_status_code",
    (
        ("multipolygon_buildings", "Polygon", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("multipolygon_buildings", "MultiPolygon", status.HTTP_200_OK),
        ("polygon_buildings", "MultiPolygon", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("polygon_buildings", "Polygon", status.HTTP_200_OK),
    ),
)
def test_polygon_params(
    endpoint: str,
    type_: str,
    expected_status_code: int,
    client: TestClient,
) -> None:
    response = client.post(
        f"/zefir_map/{endpoint}",
        json={
            "coordinates": [],
            "type": type_,
        },
    )
    assert response.status_code == expected_status_code
