import pytest
from aiohttp import ClientSession

from app.main import app
from tests.configs import NGROK_ENDPOINT



@pytest.mark_asyncio
async def test_health():
    base_url = NGROK_ENDPOINT
    async with ClientSession() as session:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        async with session.get(f"{base_url}/health/", headers=headers) as response:
            assert response.status == 200
            assert response.json() == {"status": "ok"}