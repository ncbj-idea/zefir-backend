import pytest
from fastapi.testclient import TestClient

from zefir_api.api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app=app)
