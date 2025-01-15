from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from ...models.schemas import SeriesCreate, Series, TeamInSeriesCreate, TeamInSeries
from ...services import series_service

router = APIRouter()

@router.post("/", response_model=Series)
async def create_series(
    series: SeriesCreate,
    db: Session = Depends(get_db)
):
    db_series = series_service.create_series(db=db, series=series)
    return db_series

@router.get("/{series_id}", response_model=Series)
async def get_series(series_id: int, db: Session = Depends(get_db)):
    db_series = series_service.get_series(db=db, series_id=series_id)
    if db_series is None:
        raise HTTPException(status_code=404, detail="Series not found")
    return db_series

@router.get("/", response_model=List[Series])
async def list_series(db: Session = Depends(get_db)):
    series_list = series_service.list_series(db=db)
    return series_list

@router.post("/{series_id}/teams", response_model=TeamInSeries)
async def add_team_to_series(
    series_id: int,
    team: TeamInSeries,
    db: Session = Depends(get_db)
):
    db_team = series_service.add_team_to_series(db=db, series_id=series_id, team=team)
    return db_team

@router.post("/{series_id}/teams/{team_id}/players")
async def add_player_to_team(
    series_id: int,
    team_id: int,
    player_id: int,
    db: Session = Depends(get_db)
):
    db_player = series_service.add_player_to_team(
        db=db, 
        series_id=series_id, 
        team_id=team_id, 
        player_id=player_id
    )
    return {"status": "success", "player_id": player_id}
