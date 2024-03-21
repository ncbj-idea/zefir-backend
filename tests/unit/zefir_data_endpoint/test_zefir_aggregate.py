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

import numpy as np
import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "aggregate_type, area_expected, buildings_expected",
    [
        pytest.param(
            "single_family",
            [1075000.0, 1112500.0, 1150000.0],
            [21000, 21500, 22000],
            id="single_family",
        ),
        pytest.param(
            "multi_family",
            [6000000.0, 6000000.0, 6000000.0],
            [50000, 50000, 50000],
            id="multi_family",
        ),
        pytest.param(
            "shop_service",
            [1000000.0, 1000000.0, 1000000.0],
            [20000, 20000, 20000],
            id="shop_service",
        ),
        pytest.param(
            "office",
            [],
            [],
            id="office",
        ),
        pytest.param(
            "other",
            [],
            [],
            id="other",
        ),
    ],
)
def test_get_agg_totals(
    client: TestClient,
    aggregate_type: str,
    area_expected: list[float],
    buildings_expected: list[int],
) -> None:
    response = client.get(
        "/zefir_aggregate/get_totals",
        params={"scenario_id": 0, "aggregate_type": aggregate_type},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data["total_usable_area"] == area_expected
    assert data["total_amount_of_buildings"] == buildings_expected


@pytest.mark.parametrize(
    "aggregate_type, tech_expected",
    [
        pytest.param(
            "single_family",
            {
                "LBS SF z gazem": ["Kocioł na gaz ziemny", "BATTERY_EE", "SMALL_PV"],
                "LBS SF z HP": [
                    "BATTERY_EE",
                    "SMALL_PV",
                    "HEAT_PUMP",
                    "SMALL_HEAT_STORAGE",
                ],
                "LBS SF z węglem": ["Kocioł starego typu na węgiel", "SMALL_PV"],
            },
            id="single_family",
        ),
        pytest.param(
            "multi_family",
            {
                "MF_BASIC": ["BATTERY_EE", "SMALL_PV"],
                "MF_GAS": ["BATTERY_EE", "Kocioł na gaz ziemny", "SMALL_PV"],
                "MF_HP": ["SMALL_PV", "BATTERY_EE", "HEAT_PUMP", "SMALL_HEAT_STORAGE"],
            },
            id="multi_family",
        ),
        pytest.param(
            "shop_service",
            {
                "OS_BASIC": ["SMALL_PV", "BATTERY_EE"],
                "OS_HP": ["BATTERY_EE", "SMALL_PV", "SMALL_HEAT_STORAGE", "HEAT_PUMP"],
            },
            id="shop_service",
        ),
        pytest.param(
            "office",
            [],
            id="office",
        ),
        pytest.param(
            "other",
            [],
            id="other",
        ),
    ],
)
def test_get_stacks_info(
    client: TestClient,
    aggregate_type: str,
    tech_expected: dict[str, list[str]],
) -> None:
    response = client.get(
        "/zefir_aggregate/get_stacks",
        params={"scenario_id": 0, "aggregate_type": aggregate_type},
    )
    assert response.status_code == 200
    data = response.json()
    if not data:
        assert data == tech_expected
    else:
        for obj in data:
            assert obj["stack_name"] in tech_expected
            assert sorted(obj["techs"]) == sorted(tech_expected[obj["stack_name"]])


@pytest.mark.parametrize(
    "aggregate_type, not_empty_consumption_category",
    [
        pytest.param(
            "single_family",
            ["very_high_consumption", "low_consumption"],
            id="single_family",
        ),
        pytest.param(
            "multi_family",
            ["high_consumption", "average_consumption"],
            id="multi_family",
        ),
        pytest.param(
            "shop_service",
            ["very_high_consumption"],
            id="shop_service",
        ),
        pytest.param(
            "office",
            [],
            id="office",
        ),
        pytest.param(
            "other",
            [],
            id="other",
        ),
    ],
)
def test_get_agg_details(
    client: TestClient, aggregate_type: str, not_empty_consumption_category: list[str]
) -> None:
    response = client.get(
        "/zefir_aggregate/details",
        params={"scenario_id": 0, "aggregate_type": aggregate_type},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    if not_empty_consumption_category:
        for obj in data:
            if obj["name"] in not_empty_consumption_category:
                assert len(obj["agg_area"]) == 3
                assert len(obj["agg_amount_of_building"]) == 3
                summed_values = [
                    sum(x) for x in zip(*(item["values"] for item in obj["area"]))
                ]
                assert np.allclose(np.array(summed_values), np.array(obj["agg_area"]))
