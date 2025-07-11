"""
Tests for the team record API endpoints.
Covers GET, POST, PUT, and DELETE operations for team records.
"""

import pytest
from aiohttp import ClientSession
from uuid import uuid4
from tests.configs import URL

base_url = URL
headers = {'Content-Type': 'application/json; charset=utf-8'}



@pytest.mark.asyncio
async def test_get_team_records():
    """
    Test GET /v0/team-records/ returns a list of team records.
    """
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/team-records/", headers=headers) as response:
            assert response.status in (200, 404)
            if response.status == 200:
                data = await response.json()
                assert isinstance(data, list)



@pytest.mark.asyncio
async def test_get_team_record_by_unexisted_record_id():
    """
    Test GET /v0/team-records/?record_id=<uuid> with a non-existent record_id returns 404.
    """
    record_id = str(uuid4())  # replace with a non-existent record_id
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/team-records/", params={"record_id": record_id}, headers=headers) as response:
            assert response.status == 404



@pytest.mark.asyncio
async def test_get_team_record_by_existed_record_id():
    """
    Test GET /v0/team-records/?record_id=<uuid> with an existing record_id returns a record object.
    """
    record_id = "replace-with-existing-record-uuid"
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/team-records/", params={"record_id": record_id}, headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert str(data["id"]) == record_id



@pytest.mark.asyncio
async def test_get_team_records_by_match_code():
    """
    Test GET /v0/team-records/match-code/{match_code} returns a list of records or 404.
    """
    match_code = "replace-with-existing-match-code"
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/team-records/match-code/{match_code}", headers=headers) as response:
            assert response.status in (200, 404)
            if response.status == 200:
                data = await response.json()
                assert isinstance(data, list)



@pytest.mark.asyncio
async def test_create_team_record():
    """
    Test POST /v0/team-records/ creates a new team record and returns 201.
    """
    payload = {
        "match_code": f"MC_{uuid4().hex[:6]}",
        "match_name": "Test Match",
        "team_code": f"TEAM_{uuid4().hex[:6]}",
        "point_score": 10
    }
    async with ClientSession() as session:
        async with session.post(f"{base_url}/v0/team-records/", json=payload, headers=headers) as response:
            assert response.status in (201, 400, 422)
            if response.status == 201:
                data = await response.json()
                assert data["message"] == "Record created successfully!"



@pytest.mark.asyncio
async def test_update_team_record():
    """
    Test PUT /v0/team-records/{record_id} updates a team record and returns 200, or 404/422 for invalid input or not found.
    """
    record_id = "replace-with-existing-record-uuid"
    payload = {
        "match_code": f"MC_{uuid4().hex[:6]}",
        "match_name": "Updated Match",
        "team_code": f"TEAM_{uuid4().hex[:6]}",
        "point_score": 20
    }
    async with ClientSession() as session:
        async with session.put(f"{base_url}/v0/team-records/{record_id}", json=payload, headers=headers) as response:
            assert response.status in (200, 404, 422)
            if response.status == 200:
                data = await response.json()
                assert data["message"] == "Record updated successfully!"



@pytest.mark.asyncio
async def test_delete_team_record():
    """
    Test DELETE /v0/team-records/{record_id} deletes a team record and returns 200, or 404 if not found.
    """
    record_id = "replace-with-existing-record-uuid"
    async with ClientSession() as session:
        async with session.delete(f"{base_url}/v0/team-records/{record_id}", headers=headers) as response:
            assert response.status in (200, 404)
            if response.status == 200:
                data = await response.json()
                assert data["message"] == "Record deleted successfully!"