import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "bbox, expected_ids",
    [
        pytest.param(
            [
                21.003805955045422,
                52.230679139264296,
                21.008532090428147,
                52.23271196434463,
            ],
            [5942],
            id="1 building",
        ),
        pytest.param(
            [
                20.869023197591606,
                52.18175410575409,
                20.875032709421458,
                52.1843402389807,
            ],
            [
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
            ],
            id="40 buildings",
        ),
    ],
)
def test_zefir_map_filter_by_bbox(
    client: TestClient, bbox: list[float], expected_ids: list[int]
) -> None:
    response = client.get(
        "/zefir_map/get_buildings",
        params={"bbox": bbox},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(expected_ids)
    list_of_ids = [obj["id"] for obj in data]
    assert sorted(list_of_ids) == sorted(expected_ids)


def test_zefir_map_filter_handle_huge_amount(client: TestClient) -> None:
    bbox = [
        21.059447057006928,
        52.18071951587461,
        21.21099067118059,
        52.245914444148504,
    ]
    response = client.get(
        "/zefir_map/get_buildings",
        params={"bbox": bbox},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 18504
