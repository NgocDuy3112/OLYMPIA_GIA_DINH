import pytest
from aiohttp import ClientSession
from uuid import UUID

from app.api.v0 import team
from app.schema.v0.team import TeamSchemaOut
from tests.configs import NGROK_ENDPOINT


@pytest.mark.asyncio
async def test_get_all_players():
    """
    Test GET /v0/players/ returns a list of players.
    """
    base_url = NGROK_ENDPOINT
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/") as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert all("id" in player and "name" in player for player in data)


@pytest.mark.asyncio
async def test_get_player_by_unexisted_player_id():
    """
    Test GET /v0/players/?player_id=<uuid> returns a single player.
    """
    base_url = NGROK_ENDPOINT

    # Use a known player UUID from your DB
    player_id = "b3e7bc1e-04de-4b2d-a5e0-5dc29a3c13b5"  # replace with real one

    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/", params={"player_id": player_id}) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert str(UUID(data["id"])) == player_id
            assert "name" in data


@pytest.mark.asyncio
async def test_get_player_by_unexisted_player_code():
    """
    Test GET /v0/players/player-code/{player_code} returns a player.
    """
    base_url = NGROK_ENDPOINT

    # Use a known player code from your DB
    player_code = "GLO_P_99"  # replace with real one

    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/players/player-code/{player_code}") as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert data["player_code"] == player_code
            assert "name" in data