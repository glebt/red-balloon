"""Tests for the main FastAPI application."""

import pytest
from httpx import ASGITransport, AsyncClient

from red_balloon.main import app


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """Test the root endpoint returns expected response."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Red Balloon API"
        assert "version" in data


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    """Test the health check endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
