from fastapi.testclient import TestClient


def _check_inner_data(data: list, years_len: int) -> None:
    for val_dict in data:
        tech_name, val = (val_dict["technology_name"], val_dict["values"])
        assert isinstance(tech_name, str)
        assert isinstance(val, list)
        assert len(val) == years_len
        assert all(isinstance(el, float) for el in val)


def _check_fuel_usage(data: list, years_len: int) -> None:
    for val_dict in data:
        fuel_name, usage, power = (
            val_dict["fuel_name"],
            val_dict["usage"],
            val_dict["power"],
        )
        assert isinstance(fuel_name, str)
        for val in (usage, power):
            assert isinstance(val, list)
            assert len(val) == years_len
            assert all(isinstance(el, float) for el in val)


def _check_response_json(
    data: dict,
    technology_len: int,
    emission_check: bool = False,
    fuel_usage_check: bool = False,
) -> None:
    assert data["years"] == [0, 1, 2]
    assert isinstance(data["data"], list)
    assert len(data["data"]) == technology_len
    if fuel_usage_check:
        _check_fuel_usage(data["data"], len(data["years"]))
    elif emission_check:
        for item in data["data"]:
            em_name, val = (item["emission_type"], item["data"])
            assert isinstance(em_name, str)
            _check_inner_data(val, len(data["years"]))
    else:
        _check_inner_data(data["data"], len(data["years"]))


def test_get_installed_power_version(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "installed_power"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 13)


def test_get_ee_production(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "ee_production"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 13)


def test_get_heat_production(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "heat_production"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 13)


def test_get_ee_usage(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "ee_usage"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 3)


def test_get_heat_usage(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "heat_usage"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 3)


def test_get_amount_of_devices(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "amount_of_devices"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 6)


def test_get_emissions(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "emissions"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 2, emission_check=True)


def test_get_fuel_usage(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "fuel_usage"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 3, fuel_usage_check=True)


def test_get_capex(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "capex"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 13)


def test_get_opex(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "opex"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 13)


def test_get_var_cost(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "var_cost"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 7)


def test_get_ets(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "ets"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 3)


def test_get_total_costs(client: TestClient) -> None:
    response = client.get(
        "/zefir_data/get_data",
        params={"scenario_id": 1, "data_category": "total_costs"},
    )
    assert response.status_code == 200
    data = response.json()
    _check_response_json(data, 4)
