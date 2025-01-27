from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List, Dict
from datetime import datetime
from app.models.models import roster_players_in_series, Series as SeriesModel, TeamInSeries as TeamInSeriesModel
from ..models.schemas import SeriesCreate, TeamInSeries

async def create_series(db: AsyncSession, series: SeriesCreate) -> SeriesModel:
    db_series = SeriesModel(**series.model_dump())
    db_series.created_at = datetime.now()  # Set created_at to a naive datetime
    db.add(db_series)
    try:
        await db.commit()
        await db.refresh(db_series)
        return db_series
    except IntegrityError as e:
        await db.rollback()
        raise e

async def get_series(db: AsyncSession, series_id: int) -> SeriesModel:
    result = await db.execute(select(SeriesModel).filter(SeriesModel.id == series_id))
    return result.scalar_one_or_none()

async def list_series(db: AsyncSession) -> List[SeriesModel]:
    result = await db.execute(select(SeriesModel))
    return result.scalars().all()

async def add_team_to_series(db: AsyncSession, series_id: int, team: TeamInSeries) -> TeamInSeriesModel:
    db_team = TeamInSeriesModel(series_id=series_id, **team.model_dump())
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team

async def add_player_to_team(db: AsyncSession, series_id: int, team_id: int, player_id: int) -> Dict:
    await db.execute(
        roster_players_in_series.insert().values(
            registration_id=team_id,
            player_id=player_id
        )
    )
    await db.commit()
    return {"registration_id": team_id, "player_id": player_id}

async def update_series(db: AsyncSession, series_id: int, series: SeriesCreate) -> SeriesModel:
    db_series = await get_series(db, series_id)
    if db_series is None:
        return None
    for key, value in series.model_dump().items():
        setattr(db_series, key, value)
    await db.commit()
    await db.refresh(db_series)
    return db_series

async def delete_series(db: AsyncSession, series_id: int) -> bool:
    db_series = await get_series(db, series_id)
    if db_series is None:
        return False
    await db.delete(db_series)
    await db.commit()
    return True
