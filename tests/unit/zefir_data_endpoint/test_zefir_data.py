from collections import defaultdict

from fastapi.testclient import TestClient


def test_get_data_scenario_out_of_range(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 999999999, "data_category": "installed_power"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["input"] == 999999999
    assert data["detail"][0]["msg"] == "Input should be 1, 2, 3, 4, 5, 6, 7, 8, 9 or 10"


def test_get_data_wrong_data_category(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "best_price_for_coal"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["input"] == "best_price_for_coal"
    assert (
        data["detail"][0]["msg"]
        == "Input should be 'installed_power', 'ee_production', 'heat_production', 'cold_production', "
        "'ee_usage', 'heat_usage', 'cold_usage', 'amount_of_devices', 'emissions', "
        "'fuel_usage', 'capex', 'opex', 'var_cost', 'ets' or 'total_costs'"
    )


def test_get_data_scenario_not_found_file(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 2, "data_category": "installed_power"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Scenario_id 2 not found"


def test_get_data_default_scenario_id(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"data_category": "installed_power"},
    )
    assert response.status_code == 200


def test_get_years_correct_id(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_years",
        params={"scenario_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["years"] == [0, 1, 2]


def test_get_years_id_not_found(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_years",
        params={"scenario_id": 5},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Scenario_id 5 not found"


def test_get_tags_map(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_tags_map",
    )
    assert response.status_code == 200
    data = response.json()
    assert "tags" in data
    tags = data["tags"]
    for tech_name, tag in tags.items():
        assert isinstance(tech_name, str)
        assert isinstance(tag, str)
    reversed_dict = defaultdict(list)
    for key, value in tags.items():
        reversed_dict[value].append(key)
    assert len(tags) != len(reversed_dict)
    assert len(tags) > len(reversed_dict)
