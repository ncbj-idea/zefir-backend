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

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from zefir_api.api.crud.static_plots import _get_common_sorted_indexes


@pytest.mark.parametrize(
    "input_data, expected",
    [
        pytest.param(
            {
                "df1": pd.DataFrame({"A": [1, 2, 3]}, index=["A", "B", "C"]),
                "df2": pd.DataFrame({"B": [3, 4, 1]}, index=["A", "B", "C"]),
            },
            ["A", "B", "C"],
            id="same_index",
        ),
        pytest.param(
            {
                "df1": pd.DataFrame({"A": [1, 2, 3]}, index=["A", "B", "C"]),
                "df2": pd.DataFrame({"B": [3, 4, 1]}, index=["C", "A", "B"]),
            },
            ["A", "B", "C"],
            id="not_same_index",
        ),
        pytest.param(
            {
                "df1": pd.DataFrame({"A": [1, 2, 3]}, index=[10, 20, 30]),
                "df2": pd.DataFrame({"B": [3, 4, 1]}, index=[20, 10, 30]),
            },
            [10, 20, 30],
            id="not_same_index_int",
        ),
    ],
)
def test_get_common_sorted_indexes(
    input_data: dict[str, pd.DataFrame], expected: list[str]
) -> None:
    common_indexes = _get_common_sorted_indexes(input_data)
    assert common_indexes == expected
    for df in input_data.values():
        assert df.index.to_list() == expected


def test_static_plots(client: TestClient) -> None:
    response = client.get(
        "/zefir_static/get_plots",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    assert data["labels"] == [
        "Jednorodzinne",
        "Wielorodzinne",
        "Biurowe",
        "Handlowo-usługowe",
        "Pozostałe",
    ]
    for attr in ["heat_usage", "heated_area", "gas_enable", "heat_enable", "ee_usage"]:
        assert attr in data
        assert isinstance(data[attr], list)
        for obj in data[attr]:
            assert isinstance(obj, dict)
            assert all(isinstance(key, str) for key in obj.keys())
            assert all(
                isinstance(value, list | str)
                and all(isinstance(num, float) for num in value if value is list)
                for value in obj.values()
            )
