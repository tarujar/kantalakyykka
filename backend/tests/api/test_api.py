import pytest
import respx
from httpx import Response
from tests.utils.mock_responses import (
    game_types_response, game_type_response, error_responses,
    new_game_type_response, updated_game_type_response,
    new_player_response, new_series_response, new_game_response
)
from tests.utils.mocks import (
    mock_new_game_type, mock_invalid_game_type, mock_updated_game_type,
    mock_new_player, mock_invalid_player,
    mock_new_series, mock_invalid_series,
    mock_new_game, mock_invalid_game
)

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
@respx.mock
async def test_get_game_types(async_client):
    """Test getting all game types using mocked response"""
    respx.get("http://testserver/api/v1/game_types/").mock(
        return_value=Response(200, json=game_types_response["data"])
    )
    response = await async_client.get("/api/v1/game_types/")
    
    assert response.status_code == game_types_response["status_code"]
    assert response.json() == game_types_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_get_game_type(async_client):
    """Test getting a single game type using mocked response"""
    respx.get("http://testserver/api/v1/game_types/1").mock(
        return_value=Response(200, json=game_type_response["data"])
    )
    response = await async_client.get("/api/v1/game_types/1")
    
    assert response.status_code == game_type_response["status_code"]
    assert response.json() == game_type_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_get_game_type_not_found(async_client):
    """Test getting a non-existent game type"""
    respx.get("http://testserver/api/v1/game_types/999").mock(
        return_value=Response(404, json=error_responses["not_found"])
    )
    response = await async_client.get("/api/v1/game_types/999")
    
    assert response.status_code == error_responses["not_found"]["status_code"]

@pytest.mark.asyncio
@respx.mock
async def test_create_game_type(async_client):
    """Test creating a new game type"""
    respx.post("http://testserver/api/v1/game_types/").mock(
        return_value=Response(201, json=new_game_type_response["data"])
    )
    response = await async_client.post("/api/v1/game_types/", json=mock_new_game_type)
    
    assert response.status_code == new_game_type_response["status_code"]
    assert response.json() == new_game_type_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_create_game_type_validation_error(async_client):
    """Test creating a new game type with invalid data"""
    respx.post("http://testserver/api/v1/game_types/").mock(
        return_value=Response(422, json=error_responses["validation_error"])
    )
    response = await async_client.post("/api/v1/game_types/", json=mock_invalid_game_type)
    
    assert response.status_code == 422
    assert response.json() == error_responses["validation_error"]

@pytest.mark.asyncio
@respx.mock
async def test_update_game_type(async_client):
    """Test updating an existing game type"""
    respx.put("http://testserver/api/v1/game_types/1").mock(
        return_value=Response(200, json=updated_game_type_response["data"])
    )
    response = await async_client.put("/api/v1/game_types/1", json=mock_updated_game_type)
    
    assert response.status_code == updated_game_type_response["status_code"]
    assert response.json() == updated_game_type_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_delete_game_type(async_client):
    """Test deleting an existing game type"""
    respx.delete("http://testserver/api/v1/game_types/1").mock(
        return_value=Response(204)
    )
    response = await async_client.delete("/api/v1/game_types/1")
    
    assert response.status_code == 204

@pytest.mark.asyncio
@respx.mock
async def test_get_invalid_endpoint(async_client):
    """Test accessing an invalid endpoint"""
    respx.get("http://testserver/api/v1/invalid_endpoint").mock(
        return_value=Response(404, json=error_responses["not_found"])
    )
    response = await async_client.get("/api/v1/invalid_endpoint")
    
    assert response.status_code == 404
    assert response.json() == error_responses["not_found"]

@pytest.mark.asyncio
@respx.mock
async def test_get_game_type_unauthorized(async_client):
    """Test getting a game type without authorization"""
    respx.get("http://testserver/api/v1/game_types/1").mock(
        return_value=Response(401, json={"detail": "Unauthorized"})
    )
    response = await async_client.get("/api/v1/game_types/1")
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

@pytest.mark.asyncio
@respx.mock
async def test_create_game_type_unauthorized(async_client):
    """Test creating a new game type without authorization"""
    respx.post("http://testserver/api/v1/game_types/").mock(
        return_value=Response(401, json={"detail": "Unauthorized"})
    )
    response = await async_client.post("/api/v1/game_types/", json=mock_new_game_type)
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

@pytest.mark.asyncio
@respx.mock
async def test_update_game_type_not_found(async_client):
    """Test updating a non-existent game type"""
    respx.put("http://testserver/api/v1/game_types/999").mock(
        return_value=Response(404, json=error_responses["not_found"])
    )
    response = await async_client.put("/api/v1/game_types/999", json=mock_updated_game_type)
    
    assert response.status_code == 404
    assert response.json() == error_responses["not_found"]

@pytest.mark.asyncio
@respx.mock
async def test_delete_game_type_not_found(async_client):
    """Test deleting a non-existent game type"""
    respx.delete("http://testserver/api/v1/game_types/999").mock(
        return_value=Response(404, json=error_responses["not_found"])
    )
    response = await async_client.delete("/api/v1/game_types/999")
    
    assert response.status_code == 404
    assert response.json() == error_responses["not_found"]

@pytest.mark.asyncio
@respx.mock
async def test_create_player(async_client):
    """Test creating a new player"""
    respx.post("http://testserver/api/v1/players/").mock(
        return_value=Response(201, json=new_player_response["data"])
    )
    response = await async_client.post("/api/v1/players/", json=mock_new_player)
    
    assert response.status_code == new_player_response["status_code"]
    assert response.json() == new_player_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_create_player_validation_error(async_client):
    """Test creating a new player with invalid data"""
    respx.post("http://testserver/api/v1/players/").mock(
        return_value=Response(422, json=error_responses["validation_error"])
    )
    response = await async_client.post("/api/v1/players/", json=mock_invalid_player)
    
    assert response.status_code == 422
    assert response.json() == error_responses["validation_error"]

@pytest.mark.asyncio
@respx.mock
async def test_create_series(async_client):
    """Test creating a new series"""
    respx.post("http://testserver/api/v1/series/").mock(
        return_value=Response(201, json=new_series_response["data"])
    )
    response = await async_client.post("/api/v1/series/", json=mock_new_series)
    
    assert response.status_code == new_series_response["status_code"]
    assert response.json() == new_series_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_create_series_validation_error(async_client):
    """Test creating a new series with invalid data"""
    respx.post("http://testserver/api/v1/series/").mock(
        return_value=Response(422, json=error_responses["validation_error"])
    )
    response = await async_client.post("/api/v1/series/", json=mock_invalid_series)
    
    assert response.status_code == 422
    assert response.json() == error_responses["validation_error"]

@pytest.mark.asyncio
@respx.mock
async def test_create_game(async_client):
    """Test creating a new game"""
    respx.post("http://testserver/api/v1/games/").mock(
        return_value=Response(201, json=new_game_response["data"])
    )
    response = await async_client.post("/api/v1/games/", json=mock_new_game)
    
    assert response.status_code == new_game_response["status_code"]
    assert response.json() == new_game_response["data"]

@pytest.mark.asyncio
@respx.mock
async def test_create_game_validation_error(async_client):
    """Test creating a new game with invalid data"""
    respx.post("http://testserver/api/v1/games/").mock(
        return_value=Response(422, json=error_responses["validation_error"])
    )
    response = await async_client.post("/api/v1/games/", json=mock_invalid_game)
    
    assert response.status_code == 422
    assert response.json() == error_responses["validation_error"]

@pytest.mark.asyncio
@respx.mock
async def test_server_error(async_client):
    """Test handling server errors"""
    respx.get("http://testserver/api/v1/game_types/").mock(
        return_value=Response(500, json={"detail": "Internal Server Error"})
    )
    response = await async_client.get("/api/v1/game_types/")
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}