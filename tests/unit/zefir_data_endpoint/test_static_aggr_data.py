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

from zefir_api.api.parameters import AggregateType, ConsumptionType


def test_static_aggr_data(client: TestClient) -> None:
    response = client.get(
        "/zefir_static/get_aggr_data",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for obj in data:
        assert isinstance(obj, dict)
        assert obj["aggr_type"] in AggregateType.__members__.values()
        for consumption_obj in obj["data"]:
            assert consumption_obj["consumption_type"] in ConsumptionType.__members__
            assert isinstance(consumption_obj["data"], dict)
            assert len(consumption_obj["data"]) == 3
            assert list(consumption_obj["data"].keys()) == [
                "heat_usage",
                "ee_usage",
                "cold_usage",
            ]
