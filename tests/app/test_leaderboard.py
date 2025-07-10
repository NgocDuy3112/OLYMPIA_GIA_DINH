"""
Tests for the leaderboard API endpoints.
Covers GET operations for all leaderboard types.
"""

import pytest
from aiohttp import ClientSession
from tests.configs import NGROK_ENDPOINT


base_url = NGROK_ENDPOINT
headers = {'Content-Type': 'application/json; charset=utf-8'}


LEADERBOARD_TYPES = [
    "yellow", "white", "red", "pink", "blue", "orange", "green", "team"
]


@pytest.mark.asyncio
@pytest.mark.parametrize("leaderboard_type", LEADERBOARD_TYPES)
async def test_get_leaderboard(leaderboard_type):
    """
    Test GET /v0/leaderboards/{leaderboard_type} returns a leaderboard for each type.
    """
    
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/leaderboards/{leaderboard_type}", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            # Optionally check for expected keys in the leaderboard data
            assert "items" in data or "teams" in data or "players" in data