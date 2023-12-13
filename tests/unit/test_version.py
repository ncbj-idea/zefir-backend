import pyzefir
import zefir_analytics
from fastapi.testclient import TestClient


def test_get_zefir_version(client: TestClient) -> None:
    response = client.get("/pyzefir_version")
    data = response.json()

    assert response.status_code == 200
    assert "pyzefir version" in data
    assert data["pyzefir version"] == pyzefir.__version__


def test_get_zefir_analytics_version(client: TestClient) -> None:
    response = client.get("/zefir_analytics_version")
    data = response.json()

    assert response.status_code == 200
    assert "zefir_analytics version" in data
    assert data["zefir_analytics version"] == zefir_analytics.__version__
