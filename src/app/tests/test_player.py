"""
Tests for the player API endpoints.
Covers GET operations for all players, by player_id, and by player_code.
"""

import pytest
from aiohttp import ClientSession
from uuid import UUID
from tests.configs import NGROK_ENDPOINT

base_url = NGROK_ENDPOINT
headers = {'Content-Type': 'application/json; charset=utf-8'}



@pytest.mark.asyncio
async def test_get_all_players():
    """
    Test GET /v0/players/ returns a list of players with id and name fields.
    """
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert all("id" in player and "name" in player for player in data)



@pytest.mark.asyncio
async def test_get_player_by_unexisted_player_id():
    """
    Test GET /v0/players/?player_id=<uuid> with a non-existent player_id returns 404.
    """
    player_id = "b3e7bc1e-04de-4b2d-a5e0-5dc29a3c13b5"  # replace with a non-existent player_id
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/", params={"player_id": player_id}, headers=headers) as response:
            assert response.status == 404



@pytest.mark.asyncio
async def test_get_player_by_existed_player_id():
    """
    Test GET /v0/players/?player_id=<uuid> with an existing player_id returns a player object.
    """
    player_id = "b3e7bc1e-04de-4b2d-a5e0-5dc29a3c13b5"  # replace with an existing player_id
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/", params={"player_id": player_id}, headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert str(UUID(data["id"])) == player_id
            assert "name" in data



@pytest.mark.asyncio
async def test_get_player_by_unexisted_player_code():
    """
    Test GET /v0/players/player-code/{player_code} with a non-existent player_code returns 404.
    """
    player_code = "GLO_P_99"  # replace with a non-existent player_code
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/player-code/{player_code}", headers=headers) as response:
            assert response.status == 404



@pytest.mark.asyncio
async def test_get_player_by_existed_player_code():
    """
    Test GET /v0/players/player-code/{player_code} with an existing player_code returns a player object.
    """
    player_code = "GLO_P_01"  # replace with an existing player_code
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/player-code/{player_code}", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert data["player_code"] == player_code
            assert "player_name" in data