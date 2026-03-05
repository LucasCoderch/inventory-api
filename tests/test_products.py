import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data


@pytest.mark.asyncio
async def test_create_and_get_product():
    payload = {
        "sku": "TEST-SKU-001",
        "name": "Test Product",
        "description": "Test",
        "price": 1234.5,
        "stock": 5,
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create
        r = await ac.post("/api/v1/products", json=payload)
        assert r.status_code == 201, r.text
        created = r.json()
        assert created["sku"] == payload["sku"]

        product_id = created["id"]

        # get
        r = await ac.get(f"/api/v1/products/{product_id}")
        assert r.status_code == 200
        fetched = r.json()
        assert fetched["id"] == product_id
        assert fetched["sku"] == payload["sku"]
