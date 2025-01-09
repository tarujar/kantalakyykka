from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from ...models import GameType, GameTypeCreate
from ...services import game_types_service

router = APIRouter()

@router.post("/", response_model=GameType)
async def create_game_type(
    game_type: GameTypeCreate,
    db: Session = Depends(get_db)
):
    db_game_type = game_types_service.create_game_type(db=db, game_type=game_type)
    return db_game_type

@router.get("/{game_type_id}", response_model=GameType)
async def get_game_type(game_type_id: int, db: Session = Depends(get_db)):
    db_game_type = game_types_service.get_game_type(db=db, game_type_id=game_type_id)
    if db_game_type is None:
        raise HTTPException(status_code=404, detail="Game type not found")
    return db_game_type

@router.get("/", response_model=List[GameType])
async def list_game_types(db: Session = Depends(get_db)):
    game_types = game_types_service.list_game_types(db=db)
    return game_types

@router.put("/{game_type_id}", response_model=GameType)
async def update_game_type(
    game_type_id: int,
    game_type: GameTypeCreate,
    db: Session = Depends(get_db)
):
    db_game_type = game_types_service.update_game_type(db=db, game_type_id=game_type_id, game_type=game_type)
    if db_game_type is None:
        raise HTTPException(status_code=404, detail="Game type not found")
    return db_game_type

@router.delete("/{game_type_id}", response_model=dict)
async def delete_game_type(game_type_id: int, db: Session = Depends(get_db)):
    success = game_types_service.delete_game_type(db=db, game_type_id=game_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game type not found")
    return {"status": "success"}
