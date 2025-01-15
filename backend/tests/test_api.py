import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from .mock_responses import game_types_response, game_type_response, error_responses

@pytest.fixture
def test_client():
    return TestClient(app)

def test_get_game_types(test_client):
    """Test getting all game types using mocked response"""
    with patch('app.services.game_types_service.list_game_types') as mock_list:
        mock_list.return_value = game_types_response["data"]
        response = test_client.get("/api/v1/game_types/")
        assert response.status_code == game_types_response["status_code"]
        assert response.json() == game_types_response["data"]

def test_get_game_type(test_client):
    """Test getting a single game type using mocked response"""
    with patch('app.services.game_types_service.get_game_type', return_value=game_type_response["data"]):
        response = test_client.get("/api/v1/game_types/1")
        assert response.status_code == game_type_response["status_code"]
        assert response.json() == game_type_response["data"]

def test_get_game_type_not_found(test_client):
    """Test getting a non-existent game type"""
    with patch('app.services.game_types_service.get_game_type', return_value=None):
        response = test_client.get("/api/v1/game_types/999")
        assert response.status_code == error_responses["not_found"]["status_code"]