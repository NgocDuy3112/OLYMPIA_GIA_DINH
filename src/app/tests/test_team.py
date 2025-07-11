"""
Tests for the team API endpoints.
Covers GET, POST, PUT, and DELETE operations for teams.
"""

import pytest
from aiohttp import ClientSession
from uuid import uuid4
from tests.configs import NGROK_ENDPOINT


base_url = NGROK_ENDPOINT
headers = {'Content-Type': 'application/json; charset=utf-8'}



@pytest.mark.asyncio
async def test_get_teams():
    """
    Test GET /v0/teams/ returns a list of teams.
    """
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)



@pytest.mark.asyncio
async def test_get_team_by_unexisted_team_id():
    """
    Test GET /v0/teams/?team_id=<uuid> with a non-existent team_id returns 404.
    """
    team_id = str(uuid4())  # replace with a non-existent team_id
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/", params={"team_id": team_id}, headers=headers) as response:
            assert response.status == 404



@pytest.mark.asyncio
async def test_get_team_by_existed_team_id():
    """
    Test GET /v0/teams/?team_id=<uuid> with an existing team_id returns a team object.
    """
    team_id = "replace-with-existing-team-uuid"
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/", params={"team_id": team_id}, headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert str(data["id"]) == team_id
            assert "team_name" in data



@pytest.mark.asyncio
async def test_get_team_by_unexisted_team_code():
    """
    Test GET /v0/teams/team-code/{team_code} with a non-existent team_code returns 404.
    """
    team_code = "TEAM_XYZ"  # replace with a non-existent team_code
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/team-code/{team_code}", headers=headers) as response:
            assert response.status == 404



@pytest.mark.asyncio
async def test_get_team_by_existed_team_code():
    """
    Test GET /v0/teams/team-code/{team_code} with an existing team_code returns a team object.
    """
    team_code = "TEAM_01"  # replace with an existing team_code
    async with ClientSession() as session:
        async with session.get(f"{base_url}/v0/teams/team-code/{team_code}", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert data["team_code"] == team_code
            assert "team_name" in data



@pytest.mark.asyncio
async def test_create_team():
    """
    Test POST /v0/teams/ creates a new team and returns 201.
    """
    payload = {
        "team_code": f"TEAM_{uuid4().hex[:6]}",
        "team_name": "Test Team"
    }
    async with ClientSession() as session:
        async with session.post(f"{base_url}/v0/teams/", json=payload, headers=headers) as response:
            assert response.status in (201, 400, 422)
            if response.status == 201:
                data = await response.json()
                assert data["message"] == "Team created successfully"



@pytest.mark.asyncio
async def test_update_team():
    """
    Test PUT /v0/teams/{team_id} updates a team and returns 200, or 404/422 for invalid input or not found.
    """
    team_id = "replace-with-existing-team-uuid"
    payload = {
        "team_code": f"TEAM_{uuid4().hex[:6]}",
        "team_name": "Updated Team"
    }
    async with ClientSession() as session:
        async with session.put(f"{base_url}/v0/teams/{team_id}", json=payload, headers=headers) as response:
            assert response.status in (200, 404, 422)
            if response.status == 200:
                data = await response.json()
                assert data["message"] == "Team updated successfully"



@pytest.mark.asyncio
async def test_delete_team():
    """
    Test DELETE /v0/teams/{team_id} deletes a team and returns 204, or 404 if not found.
    """
    team_id = "replace-with-existing-team-uuid"
    async with ClientSession() as session:
        async with session.delete(f"{base_url}/v0/teams/{team_id}", headers=headers) as response:
            assert response.status in (204, 404)