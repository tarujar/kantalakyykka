from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.database import get_db
from ...models.schemas import GameType as GameTypeSchema, GameTypeCreate  # Update this import
from ...services import game_types_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=GameTypeSchema)  # Use GameTypeSchema
async def create_game_type(
    game_type: GameTypeCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        db_game_type = await game_types_service.create_game_type(db=db, game_type=game_type)
        return db_game_type
    except Exception as e:
        logger.error(f"Error creating game type: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{game_type_id}", response_model=GameTypeSchema)  # Use GameTypeSchema
async def get_game_type(game_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_game_type = await game_types_service.get_game_type(db=db, game_type_id=game_type_id)
        if db_game_type is None:
            raise HTTPException(status_code=404, detail="Game type not found")
        return db_game_type
    except Exception as e:
        logger.error(f"Error fetching game type: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[GameTypeSchema])  # Use GameTypeSchema
async def list_game_types(db: AsyncSession = Depends(get_db)):
    try:
        game_types = await game_types_service.list_game_types(db=db)
        return game_types
    except Exception as e:
        logger.error(f"Error fetching game types: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{game_type_id}", response_model=GameTypeSchema)  # Use GameTypeSchema
async def update_game_type(
    game_type_id: int,
    game_type: GameTypeCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        db_game_type = await game_types_service.update_game_type(db=db, game_type_id=game_type_id, game_type=game_type)
        if db_game_type is None:
            raise HTTPException(status_code=404, detail="Game type not found")
        return db_game_type
    except Exception as e:
        logger.error(f"Error updating game type: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{game_type_id}", response_model=dict)
async def delete_game_type(game_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        success = await game_types_service.delete_game_type(db=db, game_type_id=game_type_id)
        if not success:
            raise HTTPException(status_code=404, detail="Game type not found")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error deleting game type: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
