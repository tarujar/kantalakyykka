from sqlalchemy.orm import Session
from typing import List
from ..models import Series as SeriesModel, TeamInSeries as TeamInSeriesModel, RosterPlayer as RosterPlayerModel,  SeriesCreate, TeamInSeries, RosterPlayer

def create_series(db: Session, series: SeriesCreate) -> SeriesModel:
    db_series = SeriesModel(**series.model_dump())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

def get_series(db: Session, series_id: int) -> SeriesModel:
    return db.query(SeriesModel).filter(SeriesModel.id == series_id).first()

def list_series(db: Session) -> List[SeriesModel]:
    return db.query(SeriesModel).all()

def add_team_to_series(db: Session, series_id: int, team: TeamInSeries) -> TeamInSeriesModel:
    db_team = TeamInSeriesModel(series_id=series_id, **team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def add_player_to_team(db: Session, series_id: int, team_id: int, player: RosterPlayer) -> RosterPlayerModel:
    db_player = RosterPlayerModel(registration_id=team_id, **player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
