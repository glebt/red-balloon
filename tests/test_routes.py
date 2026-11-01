"""Tests for API routes."""

import pytest
from httpx import ASGITransport, AsyncClient

from red_balloon.main import app


@pytest.mark.asyncio
async def test_get_data_info() -> None:
    """Test data info endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "data_file" in data
        assert "exists" in data
        assert "description" in data


@pytest.mark.asyncio
async def test_root_shows_data_status() -> None:
    """Test root endpoint shows data file status."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "data_file" in data
        assert "data_loaded" in data
