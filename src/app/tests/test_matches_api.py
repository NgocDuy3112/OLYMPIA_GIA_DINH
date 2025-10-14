import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_post_match_success(mocker: MockerFixture):
    mocker.patch(
        "app.api.match.post_match_to_db",
        new=mocker.AsyncMock(return_value={"response": {"messsage": "Add a match success"}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.post("/matches/", json={"match_code": "M01", "match_name": "Round 1"})

    assert resp.status_code == 200
    assert "response" in resp.json()


@pytest.mark.asyncio
async def test_get_all_matches(mocker: MockerFixture):
    mocker.patch(
        "app.api.match.get_all_matches_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": [{"match_name": "Round 1", "match_code": "M01", "players": [{"player_name": "Alice", "player_code": "P01"}]}]}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/matches/")

    assert resp.status_code == 200
    assert isinstance(resp.json()["response"]["data"], list)


@pytest.mark.asyncio
async def test_get_match_by_code(mocker: MockerFixture):
    mocker.patch(
        "app.api.match.get_match_from_match_code_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": {"match_code": "M01", "match_name": "Round 1", "players": [{"player_name": "Alice", "player_code": "P01"}]}}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/matches/M01")

    assert resp.status_code == 200
    assert resp.json()["response"]["data"]["match_code"] == "M01"