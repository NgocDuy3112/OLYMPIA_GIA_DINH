"""
Tests for the answer API endpoints.
Covers creating an answer and retrieving the last 3 answers.
"""

import pytest
from aiohttp import ClientSession
from decimal import Decimal

from app.api.v0 import answer
from app.schema.v0.answer import AnswerSchema
from tests.configs import URL



base_url = URL
headers = {'Content-Type': 'application/json; charset=utf-8'}


@pytest.mark.asyncio
async def test_create_answer():
    """
    Test creating an answer returns 200 and includes the answer in the response list.
    """
    payload = AnswerSchema(
        index=1,
        name="TestUser",
        answer="Sample Answer",
        time=Decimal("30.000")
    )
    async with ClientSession() as session:
        async with session.post(f"{base_url}/v0/answers/", json=payload.model_dump(mode="json"), headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert any(item.get("answer") == "Sample Answer" for item in data)

@pytest.mark.asyncio
async def test_get_answers_limit():
    """
    Test retrieving answers returns last 3 answers with correct structure.
    """
    answer.answers.clear()  # clear in-memory list before test
    async with ClientSession() as session:
        for i in range(5):
            payload = AnswerSchema(
                index=(i % 3) + 1,
                name=f"Player{i}",
                answer=f"Answer {i}",
                time=Decimal(f"{i+1}.000")
            )
            await session.post(f"{base_url}/v0/answers/", json=payload.model_dump(mode="json"), headers=headers)

        async with session.get(f"{base_url}/v0/answers/", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert len(data) == 3
            expected = ["Answer 2", "Answer 3", "Answer 4"]
            actual = [item["answer"] for item in data]
            assert actual == expected