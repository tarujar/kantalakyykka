from fastapi import HTTPException
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import GameType, Player

async def get_max_players_for_game_type(session: AsyncSession, game_type: GameType) -> int:
    result = await session.execute(select(GameType).filter_by(name=game_type.value))
    game_type_record = result.scalar_one_or_none()
    if game_type_record is None:
        raise HTTPException(status_code=404, detail="Game type not found")
    return game_type_record.max_players

async def validate_game_players(session: AsyncSession, game_type: GameType, players: List[Player]) -> None:
    max_players = await get_max_players_for_game_type(session, game_type)
    if len(players) > max_players:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {max_players} players allowed in {game_type.value} series"
        )

async def calculate_game_score(team_score: int, points_multiplier: int) -> int:
    return team_score * points_multiplier 

def calculate_throw_points(throw_input: str) -> tuple[int, str | None]:
    """Laskee heiton pisteet ja tyypin syötteen perusteella.
    
    Sallitut syötteet:
    - Numero väliltä -8..80: suora pistemäärä
    - H: hauki (ei osumaa, 0 pistettä)
    - -: hylätty (0 pistettä)
    - U: käyttämätön (0 pistettä)
    """
    match throw_input:
        case 'H':
            return (0, 'H')      # Ei osumaa
        case '-':
            return (0, '-')      # Hylätty
        case 'U':
            return (0, 'U')      # Käyttämätön
        case _:
            try:
                points = int(throw_input)
                if -8 <= points <= 80:  # Sallittu pistemäärä
                    return (points, None)
                raise ValueError("Points must be between -8 and 80")
            except ValueError:
                raise ValueError(f"Invalid throw input: {throw_input}")