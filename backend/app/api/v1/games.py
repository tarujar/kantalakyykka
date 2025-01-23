from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.database import get_db
from ...models.schemas import Game as GameSchema, GameCreate  # Update this import
from ...services import game_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=GameSchema)  # Use GameSchema
async def create_game(
    game: GameCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        db_game = await game_service.create_game(db=db, game=game)
        return db_game
    except Exception as e:
        logger.error(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{game_id}", response_model=GameSchema)  # Use GameSchema
async def get_game(game_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_game = await game_service.get_game(db=db, game_id=game_id)
        if db_game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return db_game
    except Exception as e:
        logger.error(f"Error fetching game: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[GameSchema])  # Use GameSchema
async def list_games(db: AsyncSession = Depends(get_db)):
    try:
        games = await game_service.list_games(db=db)
        return games
    except Exception as e:
        logger.error(f"Error fetching games: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{game_id}", response_model=GameSchema)  # Use GameSchema
async def update_game(
    game_id: int,
    game: GameCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        db_game = await game_service.update_game(db=db, game_id=game_id, game=game)
        if db_game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return db_game
    except Exception as e:
        logger.error(f"Error updating game: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{game_id}", response_model=dict)
async def delete_game(game_id: int, db: AsyncSession = Depends(get_db)):
    try:
        success = await game_service.delete_game(db=db, game_id=game_id)
        if not success:
            raise HTTPException(status_code=404, detail="Game not found")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error deleting game: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
