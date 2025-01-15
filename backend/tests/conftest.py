import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient() as client:
        app_client = TestClient(app)
        client.base_url = "http://testserver"
        client.app = app_client.app
        yield client

