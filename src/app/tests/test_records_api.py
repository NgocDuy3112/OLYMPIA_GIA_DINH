import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_post_record_success(mocker: MockerFixture):
    mocker.patch(
        "app.api.record.post_record_to_db",
        new=mocker.AsyncMock(return_value={"response": {"message": "Add a record successfully!"}})
    )

    payload = {"match_code": "M01", "player_code": "P01", "d_score_earned": 10}
    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.post("/records/", json=payload)

    assert resp.status_code == 200
    assert "response" in resp.json()


@pytest.mark.asyncio
async def test_get_records_by_player_code(mocker: MockerFixture):
    mocker.patch(
        "app.api.record.get_all_records_from_player_code_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": {"player_code": "P01", "records": [{"match_code": "M01", "d_score_earned": 10}]}}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/records/", params={"player_code": "P01"})

    assert resp.status_code == 200
    assert resp.json()["response"]["data"]["player_code"] == "P01"