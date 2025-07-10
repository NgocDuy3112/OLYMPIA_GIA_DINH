import pytest
from aiohttp import ClientSession

from app.main import app
from tests.configs import NGROK_ENDPOINT


base_url = NGROK_ENDPOINT



@pytest.mark.asyncio
async def test_health():
    """
    Testing if when server is healthy by checking the status code and the json content.
    """
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    async with ClientSession() as session:
        async with session.get(f"{base_url}/health/", headers=headers) as response:
            assert response.status == 200
            assert response.json() == {"status": "ok"}