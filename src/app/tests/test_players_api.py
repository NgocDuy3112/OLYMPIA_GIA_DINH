import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_post_player_success(mocker: MockerFixture):
    mocker.patch(
        "app.api.player.post_player_to_db",
        new=mocker.AsyncMock(return_value={"response": {"messsage": "Add a player success"}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.post("/players/", json={"team_code": "T01", "player_code": "P01", "player_name": "Alice"})

    assert resp.status_code == 200
    body = resp.json()
    assert "response" in body
    assert "messsage" in body["response"]


@pytest.mark.asyncio
async def test_get_all_players(mocker: MockerFixture):
    mocker.patch(
        "app.api.player.get_all_players_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": [{"player_name": "Alice", "team_name": "Team A"}]}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/players/")

    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body["response"]["data"], list)


@pytest.mark.asyncio
async def test_get_player_by_code(mocker: MockerFixture):
    mocker.patch(
        "app.api.player.get_player_from_player_code_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": {"player_name": "Alice", "team_name": "Team A"}}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/players/P01")

    assert resp.status_code == 200
    assert resp.json()["response"]["data"]["player_name"] == "Alice"