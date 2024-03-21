# NCBR_backend
# Copyright (C) 2024 Narodowe Centrum Badań Jądrowych
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


def test_get_areas(client: TestClient) -> None:
    response = client.get("/areas")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2
    assert len(response_json[1]["scenarios"]) == 2


def test_get_area_scenarios(client: TestClient) -> None:
    response = client.get("/areas/0")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert set(response_json[0].keys()) == {"description", "id", "name"}


def test_get_incorrect_area_scenarios(client: TestClient) -> None:
    response = client.get("/areas/999")
    assert response.status_code == 404
