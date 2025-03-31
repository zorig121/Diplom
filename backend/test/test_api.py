# tests/test_api.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/register", json={
            "username": "testuser",
            "password": "testpass",
            "email": "test@test.com",
            "fullname": "Test User"
        })
        assert r.status_code == 200
        token = r.json()["access_token"]

        r2 = await ac.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        assert r2.status_code == 200
        assert r2.json()["username"] == "testuser"
