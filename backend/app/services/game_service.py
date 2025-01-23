from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from ..models.models import Game as GameModel, GameType as GameTypeModel
from ..models.schemas import GameCreate, Game


async def calculate_game_score(team_score: int, points_multiplier: int) -> int:
    if points_multiplier not in [1, 2]:
        raise ValueError("Invalid season")
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

async def create_game(db: AsyncSession, game: GameCreate) -> Game:
    await validate_game_players(db, game.game_type_id, game.players)
    db_game = GameModel(
        series_id=game.series_id,
        round=game.round,
        is_playoff=game.is_playoff,
        game_date=game.game_date,
        team_1_id=game.team_1_id,
        team_2_id=game.team_2_id,
        score_1_1=game.score_1_1,
        score_1_2=game.score_1_2,
        score_2_1=game.score_2_1,
        score_2_2=game.score_2_2,
    )
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def get_game(db: AsyncSession, game_id: int) -> Game:
    result = await db.execute(select(GameModel).filter(GameModel.id == game_id))
    db_game = result.scalars().first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

async def list_games(db: AsyncSession) -> list[GameModel]:
    result = await db.execute(select(GameModel))
    return result.scalars().all()

async def validate_game_players(db: AsyncSession, game_type_id: int, players: list[int]):
    result = await db.execute(select(GameTypeModel).filter(GameTypeModel.id == game_type_id))
    game_type = result.scalars().first()
    if not game_type:
        raise HTTPException(status_code=400, detail="Invalid game type")
    
    max_players = game_type.max_players
    if len(players) > max_players:
        raise HTTPException(status_code=400, detail="Too many players for this game type")
    if len(players) < max_players:
        raise HTTPException(status_code=400, detail="Not enough players for this game type")

async def update_game(db: AsyncSession, game_id: int, game: GameCreate) -> Game:
    db_game = await get_game(db, game_id)
    if db_game is None:
        return None
    for key, value in game.model_dump().items():
        setattr(db_game, key, value)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def delete_game(db: AsyncSession, game_id: int) -> bool:
    db_game = await get_game(db, game_id)
    if db_game is None:
        return False
    await db.delete(db_game)
    await db.commit()
    return True