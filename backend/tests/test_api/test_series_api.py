import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.models import SeriesRegistration, Series, GameType, Player
from app.services.series_service import SeriesService  # Import the actual service class

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session

@pytest.fixture
def series_service():
    return SeriesService()

@pytest.fixture
def series_data():
    return {
        "name": "Test Series",
        "season_type": "winter",
        "year": 2024,
        "game_type_id": 1
    }

@pytest.mark.asyncio
async def test_create_series(async_client, async_session, series_data):  # Changed from mock_async_session
    # Mock execution results
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = None  # No duplicate series
    
    with patch.object(async_session, 'execute', new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_result
        
        response = await async_client.post("/api/v1/series/", json=series_data)
        assert response.status_code == 200
        assert response.json()["name"] == series_data["name"]

@pytest.mark.asyncio
async def test_add_player_to_team(async_session):  # Changed to use async_session
    # Test data
    registration_id = 1
    player_id = 1
    
    # Mock query results
    mock_registration = Mock(SeriesRegistration)
    mock_registration.id = registration_id
    mock_player = Mock(Player)
    mock_player.id = player_id
    
    with patch.object(async_session, 'execute', new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value.scalar_one_or_none.side_effect = [
            mock_registration,
            mock_player,
            None
        ]
        
        service = SeriesService()
        result = await service.add_player_to_team(
            session=async_session,
            team_id=registration_id,
            player_id=player_id
        )
        
        assert result["status"] == "success"
        assert result["player_id"] == player_id
