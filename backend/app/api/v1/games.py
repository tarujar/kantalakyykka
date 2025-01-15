from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.database import get_db
from ...models import GameCreate, Game
from ...services import game_service

router = APIRouter()

@router.post("/", response_model=Game)
async def create_game(
    game: GameCreate,
    db: AsyncSession = Depends(get_db)
):
    db_game = await game_service.create_game(db=db, game=game)
    return db_game

@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, db: AsyncSession = Depends(get_db)):
    db_game = await game_service.get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.get("/", response_model=List[Game])
async def list_games(db: AsyncSession = Depends(get_db)):
    games = await game_service.list_games(db=db)
    return games
