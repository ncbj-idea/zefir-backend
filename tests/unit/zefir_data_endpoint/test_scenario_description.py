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


def test_get_scenario_description(client: TestClient) -> None:
    response = client.get(
        "/zefir_static/get_scenario_description",
    )
    expected_response = {
        "id": 0,
        "name": "scenario_1",
        "total_cost": 2885025053926.2666,
        "total_capex": 8263967.174171254,
        "total_opex": 12617487336.504877,
        "total_varcost": 2872377162642.3433,
        "total_emission_CO2": 2281083.9112171233,
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dolor quis urna",
        "analyze_time": 5,
        "analyze_step": 1,
    }
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert isinstance(data[0].pop("date"), str)
    assert isinstance(data[0], dict)
    assert data[0] == expected_response
