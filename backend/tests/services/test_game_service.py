import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from app.services import game_service 
from tests.utils.mocks import mock_game_data, mock_invalid_game_data, mock_game_response, mock_games_list_response

@pytest_asyncio.fixture
async def db_session(async_session: AsyncSession):
    yield async_session

@pytest.mark.asyncio(loop_scope="session")
async def test_calculate_game_score():
    assert await game_service.calculate_game_score(-23, 1) == -23  # Kesä
    assert await game_service.calculate_game_score(-23, 2) == -46  # Talvi

@pytest.mark.asyncio
async def test_calculate_game_score_zero():
    assert await game_service.calculate_game_score(0, 1) == 0  # Kesä
    assert await game_service.calculate_game_score(0, 2) == 0  # Talvi

@pytest.mark.asyncio
async def test_calculate_game_score_positive():
    assert await game_service.calculate_game_score(10, 1) == 10  # Kesä
    assert await game_service.calculate_game_score(10, 2) == 20  # Talvi

@pytest.mark.asyncio
async def test_calculate_game_score_invalid_season():
    with pytest.raises(ValueError):
        await game_service.calculate_game_score(10, 3)  # Invalid season

@pytest.mark.asyncio
@patch('app.services.game_service.create_game', new_callable=AsyncMock)
async def test_create_game(mock_create_game, db_session):
    mock_create_game.return_value = mock_game_response
    game = await game_service.create_game(db_session, mock_game_data)
    assert game["series_id"] == mock_game_data["series_id"]
    assert game["team_1_id"] == mock_game_data["team_1_id"]
    assert game["team_2_id"] == mock_game_data["team_2_id"]

@pytest.mark.asyncio
@patch('app.services.game_service.create_game', new_callable=AsyncMock)
async def test_create_game_invalid_teams(mock_create_game, db_session):
    mock_create_game.side_effect = ValueError("team_1_id and team_2_id must be different")
    with pytest.raises(ValueError):
        await game_service.create_game(db_session, mock_invalid_game_data)

@pytest.mark.asyncio
@patch('app.services.game_service.get_game', new_callable=AsyncMock)
async def test_get_game(mock_get_game, db_session):
    game_id = 1
    mock_get_game.return_value = mock_game_response
    game = await game_service.get_game(db_session, game_id)
    assert game["id"] == game_id

@pytest.mark.asyncio
@patch('app.services.game_service.get_game', new_callable=AsyncMock)
async def test_get_game_not_found(mock_get_game, db_session):
    game_id = 999
    mock_get_game.side_effect = HTTPException(status_code=404, detail="Game not found")
    with pytest.raises(HTTPException):
        await game_service.get_game(db_session, game_id)

@pytest.mark.asyncio
@patch('app.services.game_service.list_games', new_callable=AsyncMock)
async def test_list_games(mock_list_games, db_session):
    mock_list_games.return_value = mock_games_list_response
    games = await game_service.list_games(db_session)
    assert len(games) > 0