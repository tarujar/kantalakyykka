from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List
from database.database import get_db
from ...models.schemas import SeriesCreate, Series, SeriesRegistrationCreate, SeriesRegistration
from ...services import series_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Series)
async def create_series(
    name: str = Form(...),
    season_type: str = Form(...),
    year: int = Form(...),
    status: str = Form("upcoming"),
    registration_open: bool = Form(True),
    game_type_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    series = SeriesCreate(
        name=name,
        season_type=season_type,
        year=year,
        status=status,
        registration_open=registration_open,
        game_type_id=game_type_id
    )
    try:
        db_series = await series_service.create_series(db=db, series=series)
        return db_series
    except IntegrityError as e:
        logger.error(f"Error creating series: {e}")
        raise HTTPException(status_code=400, detail="Series with the same NAME and YEAR already exists")
    except Exception as e:
        logger.error(f"Error creating series: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{series_id}", response_model=Series)
async def get_series(series_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_series = await series_service.get_series(db=db, series_id=series_id)
        if db_series is None:
            raise HTTPException(status_code=404, detail="Series not found")
        return db_series
    except Exception as e:
        logger.error(f"Error fetching series: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[Series])
async def list_series(db: AsyncSession = Depends(get_db)):
    try:
        series_list = await series_service.list_series(db=db)  # Ensure this is awaited
        return series_list
    except Exception as e:
        logger.error(f"Error fetching series: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/{series_id}/teams", response_model=SeriesRegistration)
async def add_team_to_series(
    series_id: int,
    team: SeriesRegistration,
    db: AsyncSession = Depends(get_db)
):
    db_team = await series_service.add_team_to_series(db=db, series_id=series_id, team=team)
    return db_team

@router.post("/{series_id}/teams/{team_id}/players")
async def add_player_to_team(
    series_id: int,
    team_id: int,
    player_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_player = await series_service.add_player_to_team(
        db=db, 
        series_id=series_id, 
        team_id=team_id, 
        player_id=player_id
    )
    return {"status": "success", "player_id": player_id}
