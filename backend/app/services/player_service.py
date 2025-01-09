from sqlalchemy.orm import Session
from ..models.schemas import PlayerCreate, Player

def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, player_id: int) -> Player:
    return db.query(Player).filter(Player.id == player_id).first()

def list_players(db: Session) -> list[Player]:
    return db.query(Player).all()

def update_player(db: Session, player_id: int, player: PlayerCreate) -> Player:
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if db_player:
        for key, value in player.dict().items():
            setattr(db_player, key, value)
        db.commit()
        db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int) -> bool:
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
        return True
    return False
