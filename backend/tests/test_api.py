import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("game_type, players, points_multiplier, expected_status", [
    ("single", [1], 1, 200),
    ("single", [1, 2], 1, 400),  # Invalid case: too many players for single game type
    ("team", [1, 2], 1, 200),
    ("team", [1], 1, 400),  # Invalid case: not enough players for team game type
])
def test_create_game(game_type, players, points_multiplier, expected_status):
    response = client.post("/api/v1/games/", json={
        "game_type": game_type,
        "players": players,
        "points_multiplier": points_multiplier
    })
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()["status"] == "success"
    else:
        assert response.json()["detail"] is not None