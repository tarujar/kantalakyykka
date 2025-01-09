from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from ...models.schemas import PlayerCreate, Player
from ...services import player_service

router = APIRouter()

@router.post("/", response_model=Player)
async def create_player(
    player: PlayerCreate,
    db: Session = Depends(get_db)
):
    db_player = player_service.create_player(db=db, player=player)
    return db_player

@router.get("/{player_id}", response_model=Player)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    db_player = player_service.get_player(db=db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@router.get("/", response_model=List[Player])
async def list_players(db: Session = Depends(get_db)):
    players = player_service.list_players(db=db)
    return players

@router.put("/{player_id}", response_model=Player)
async def update_player(
    player_id: int,
    player: PlayerCreate,
    db: Session = Depends(get_db)
):
    db_player = player_service.update_player(db=db, player_id=player_id, player=player)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@router.delete("/{player_id}", response_model=dict)
async def delete_player(player_id: int, db: Session = Depends(get_db)):
    success = player_service.delete_player(db=db, player_id=player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"status": "success"}
