"""
Tests for the player record API endpoints in the record_player module.
Covers GET, POST, PUT, and DELETE operations for player records.
"""

import pytest
from aiohttp import ClientSession
from uuid import uuid4
from tests.configs import NGROK_ENDPOINT



base_url = NGROK_ENDPOINT
headers = {'Content-Type': 'application/json; charset=utf-8'}



@pytest.mark.asyncio
async def test_get_player_records():
    """
    Test retrieving all player records returns 200 or 404 and correct structure if found.
    """
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/player-records/", headers=headers) as resp:
            assert resp.status in (200, 404)
            if resp.status == 200:
                data = await resp.json()
                assert isinstance(data, list)
                if data:
                    assert 'match_name' in data[0]
                    assert 'player_name' in data[0]
                    assert 'point_score' in data[0]



@pytest.mark.asyncio
async def test_get_player_records_by_match_code():
    """
    Test retrieving player records by match_code returns 200 or 404 and correct structure if found.
    """
    match_code = "test-match-code"  # Replace with a valid match_code
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/player-records/match-code/{match_code}", headers=headers) as resp:
            assert resp.status in (200, 404)
            if resp.status == 200:
                data = await resp.json()
                assert isinstance(data, list)
                if data:
                    assert 'match_name' in data[0]
                    assert 'player_name' in data[0]
                    assert 'point_score' in data[0]



@pytest.mark.asyncio
async def test_create_player_record():
    """
    Test creating a player record returns 201 and success message, or 400/422 for invalid input.
    """
    payload = {
        "match_code": str(uuid4()),
        "match_name": "Test Match",
        "player_code": str(uuid4()),
        "point_score": 10
    }
    async with ClientSession() as session:
        async with session.post(f"{base_url}/v0/player-records/", json=payload, headers=headers) as resp:
            assert resp.status in (201, 400, 422)
            if resp.status == 201:
                data = await resp.json()
                assert data["message"] == "Record created successfully!"



@pytest.mark.asyncio
async def test_update_player_record():
    """
    Test updating a player record returns 200 and success message, or 404/422 for invalid input or not found.
    """
    record_id = str(uuid4())  # Replace with a valid record_id
    payload = {
        "match_code": str(uuid4()),
        "match_name": "Updated Match",
        "player_code": str(uuid4()),
        "point_score": 15
    }
    async with ClientSession() as session:
        async with session.put(f"{base_url}/v0/player-records/{record_id}", json=payload, headers=headers) as resp:
            assert resp.status in (200, 404, 422)
            if resp.status == 200:
                data = await resp.json()
                assert data["message"] == "Record updated successfully!"



@pytest.mark.asyncio
async def test_delete_player_record():
    """
    Test deleting a player record returns 200 and success message, or 404 if not found.
    """
    record_id = str(uuid4())  # Replace with a valid record_id
    async with ClientSession() as session:
        async with session.delete(f"{base_url}/v0/player-records/{record_id}", headers=headers) as resp:
            assert resp.status in (200, 404)
            if resp.status == 200:
                data = await resp.json()
                assert data["message"] == "Record deleted successfully!"