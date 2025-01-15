import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import game_service 
from .mocks import mock_game_type_single, mock_player_1, mock_player_2

@pytest_asyncio.fixture
async def db_session(async_session: AsyncSession):
    yield async_session


@pytest.mark.asyncio(loop_scope="session")
async def test_calculate_game_score():
    assert await game_service.calculate_game_score(-23, 1) == -23  # Kesä
    assert await game_service.calculate_game_score(-23, 2) == -46  # Talvi