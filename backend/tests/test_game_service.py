import pytest
from app.services import game_service
from app.models.schemas import GameType
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_validate_game_players_single():
    # Valid case
    await game_service.validate_game_players(GameType.SINGLE, [{"id": 1}])
    
    # Invalid case
    with pytest.raises(HTTPException) as exc:
        await game_service.validate_game_players(GameType.SINGLE, [{"id": 1}, {"id": 2}])
    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_calculate_game_score():
    assert await game_service.calculate_game_score(-23, 1) == -23  # Kesä
    assert await game_service.calculate_game_score(-23, 2) == -46  # Talvi 