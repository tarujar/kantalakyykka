from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_game():
    response = client.post("/api/v1/games/", json={
        "game_type": "single",
        "players": [1],
        "points_multiplier": 1
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success" 