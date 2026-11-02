"""Integration tests for API endpoints with real data."""

import pytest
from httpx import ASGITransport, AsyncClient

from red_balloon.main import app


@pytest.mark.asyncio
async def test_get_years() -> None:
    """Test years endpoint returns list of years."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/years")
        assert response.status_code == 200
        years = response.json()
        assert isinstance(years, list)
        if years:  # If data exists
            assert all(isinstance(year, int) for year in years)
            assert years == sorted(years)  # Should be sorted


@pytest.mark.asyncio
async def test_get_cameras() -> None:
    """Test cameras endpoint returns camera list with counts."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/cameras")
        assert response.status_code == 200
        cameras = response.json()
        assert isinstance(cameras, dict)
        if cameras:  # If data exists
            # Check all values are integers (counts)
            assert all(isinstance(count, int) for count in cameras.values())
            # Check sorted by count (descending)
            counts = list(cameras.values())
            assert counts == sorted(counts, reverse=True)
