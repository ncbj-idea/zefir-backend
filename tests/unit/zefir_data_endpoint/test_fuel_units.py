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

from fastapi.testclient import TestClient


def test_fuel_units(client: TestClient) -> None:
    expected_units = {"Gaz": "m3", "Węgiel": "t", "Biomasa": "kg"}
    response = client.get(
        url="/zefir_data/get_fuel_units",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for fuel in data:
        fuel_name = fuel.get("fuel_name")
        assert fuel_name in expected_units
        assert fuel.get("fuel_unit") == expected_units[fuel_name]
