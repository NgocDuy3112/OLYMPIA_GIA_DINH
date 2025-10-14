import pytest
import time
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_post_answer_success(mocker: MockerFixture):
    mocker.patch(
        "app.api.answer.post_answer_to_db",
        new=mocker.AsyncMock(return_value={"response": {"messsage": "Add an answer successfully!"}})
    )

    payload = {"player_code": "P01", "match_code": "M01", "content": "42", "timestamp": time.time()}
    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.post("/answers/", json=payload)

    assert resp.status_code == 200
    assert "response" in resp.json()


@pytest.mark.asyncio
async def test_get_answers_by_match_code(mocker: MockerFixture):
    mocker.patch(
        "app.api.answer.get_all_answers_from_match_code_from_db",
        new=mocker.AsyncMock(return_value={"response": {"data": {"match_code": "M01", "answers": [{"content": "42", "timestamp": "2025-01-01T00:00:00", "player_code": "P01"}]}}})
    )

    async with AsyncClient(base_url=settings.BASE_URL) as ac:
        resp = await ac.get("/answers/M01")

    assert resp.status_code == 200
    assert resp.json()["response"]["data"]["match_code"] == "M01"