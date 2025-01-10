import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .mocks import mock_game_type_single, mock_player_1, mock_player_2

@pytest_asyncio.fixture
async def db_session(async_session: AsyncSession):
    yield async_session

@pytest.mark.asyncio
async def test_validate_game_players_single(db_session: AsyncSession):
    # Valid case
    await game_service.validate_game_players(db_session, mock_game_type_single, [mock_player_1])
    
    # Invalid case
    with pytest.raises(HTTPException) as exc:
        await game_service.validate_game_players(db_session, mock_game_type_single, [mock_player_1, mock_player_2])
    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_game_score():
    assert await game_service.calculate_game_score(-23, 1) == -23  # Kesä
    assert await game_service.calculate_game_score(-23, 2) == -46  # Talvi