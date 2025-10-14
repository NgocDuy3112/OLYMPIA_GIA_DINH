import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_post_team_success(mocker: MockerFixture):
    mocker.patch(
        "app.api.team.post_team_to_db",
        new=mocker.AsyncMock(return_value={"response": {"messsage": "Add a team success"}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.post("/teams/", json={"team_code": "T01", "team_name": "Team A"})

    assert resp.status_code == 200
    assert "response" in resp.json()


@pytest.mark.asyncio
async def test_get_all_teams(mocker: MockerFixture):
    mocker.patch(
        "app.api.team.get_all_teams_with_players_info_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": [{"team_name": "Team A", "team_code": "T01", "players": [{"player_name": "Alice", "player_code": "P01"}]}]}}),
        create=True
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/teams/")

    assert resp.status_code == 200
    assert isinstance(resp.json()["response"]["data"], list)


@pytest.mark.asyncio
async def test_get_team_by_code(mocker: MockerFixture):
    mocker.patch(
        "app.api.team.get_team_with_players_info_from_team_code_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": {"team_name": "Team A", "team_code": "T01", "players": [{"player_name": "Alice", "player_code": "P01"}]}}}),
        create=True
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/teams/T01")

    assert resp.status_code == 200
    data = resp.json()["response"]["data"]
    # tolerate list vs dict result (API ambiguity); normalize
    if isinstance(data, list):
        data = data[0]
    assert data["team_code"] == "T01"