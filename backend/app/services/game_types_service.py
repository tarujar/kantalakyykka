from sqlalchemy.orm import Session
from typing import List
from ..models import GameType as GameTypeModel, GameTypeCreate

def create_game_type(db: Session, game_type: GameTypeCreate) -> GameTypeModel:
    db_game_type = GameTypeModel(**game_type.model_dump())
    db.add(db_game_type)
    db.commit()
    db.refresh(db_game_type)
    return db_game_type

def get_game_type(db: Session, game_type_id: int) -> GameTypeModel:
    return db.query(GameTypeModel).filter(GameTypeModel.id == game_type_id).first()

def list_game_types(db: Session) -> List[GameTypeModel]:
    return db.query(GameTypeModel).all()
