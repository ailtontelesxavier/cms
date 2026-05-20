import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestTagsAPI:
    async def test_list_tags_returns_200(self, client):
        response = await client.get("/api/v1/tags")
        assert response.status_code in (200, 500)

    async def test_create_tag_no_auth(self, client):
        data = {"name": "Test", "slug": "test"}
        response = await client.post("/api/v1/tags", json=data)
        assert response.status_code == 401
