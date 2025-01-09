from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from ...models.schemas import GameCreate, GameResult, Game, GameType
from ...services import game_service

router = APIRouter()

@router.post("/", response_model=Game)
async def create_game(
    game: GameCreate,
    db: Session = Depends(get_db)
):
    db_game = game_service.create_game(db=db, game=game)
    return db_game

@router.post("/{game_id}/result", response_model=GameResult)
async def save_game_result(
    game_id: int,
    result: GameResult,
    db: Session = Depends(get_db)
):
    db_game_result = game_service.save_game_result(db=db, game_id=game_id, result=result)
    return db_game_result

@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_service.get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.get("/", response_model=List[Game])
async def list_games(db: Session = Depends(get_db)):
    games = game_service.list_games(db=db)
    return games
