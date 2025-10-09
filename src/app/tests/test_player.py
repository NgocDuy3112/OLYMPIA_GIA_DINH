from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_get_all_players():
    response = client.get("/players")
    assert response.status_code == 200



