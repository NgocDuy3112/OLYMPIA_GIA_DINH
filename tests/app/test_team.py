import pytest
from aiohttp import ClientSession
from decimal import Decimal

from app.main import app
from app.api.v0 import team
from app.schema.v0.team import TeamSchemaOut
from tests.configs import NGROK_ENDPOINT



@pytest.mark_asyncio
async def test_get_teams():
    base_url = NGROK_ENDPOINT
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert len(data) == 3


@pytest.mark_asyncio
async def test_get_team_by_team_id_1():
    base_url = NGROK_ENDPOINT
    