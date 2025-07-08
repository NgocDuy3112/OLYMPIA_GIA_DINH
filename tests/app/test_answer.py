import pytest
from aiohttp import ClientSession
from decimal import Decimal

from app.main import app
from app.api.v0 import answer
from app.schema.v0.answer import AnswerSchema
from tests.configs import NGROK_ENDPOINT



@pytest.mark.asyncio
async def test_create_answer():
    base_url = NGROK_ENDPOINT
    payload = AnswerSchema(
        index=1,
        name="TestUser",
        answer="Sample Answer",
        time=Decimal("30.000")
    )
    async with ClientSession() as session:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        async with session.post(f"{base_url}/v0/answers/", json=payload.model_dump(mode="json"), headers=headers) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_get_answers_limit():
    base_url = NGROK_ENDPOINT
    async with ClientSession() as session:
        answer.answers.clear()
        for i in range(5):
            payload = AnswerSchema(
                index=(i % 3) + 1,
                name=f"Player{i}",
                answer=f"Answer {i}",
                time=Decimal(f"{i+1}.000")
            )
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            await session.post(f"{base_url}/v0/answers/", json=payload.model_dump(mode="json"), headers=headers)

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        async with session.get(f"{base_url}/v0/answers/", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert len(data) == 3
            assert data[0]["answer"] == "Answer 2"
            assert data[1]["answer"] == "Answer 3"
            assert data[2]["answer"] == "Answer 4"