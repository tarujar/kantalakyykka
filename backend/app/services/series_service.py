import logging
from sqlalchemy.orm import Session
from app.models.models import RosterPlayersInSeries, Player, TeamInSeries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List, Dict
from datetime import datetime
from app.models.models import Series as SeriesModel, TeamInSeries as TeamInSeriesModel
from ..models.schemas import SeriesCreate, TeamInSeries

class SeriesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def add_player_to_team(self, session: Session, team_id: int, player_id: int) -> bool:
        """Add a player to a team's roster
        Args:
            session: SQLAlchemy session
            team_id: The ID of the team
            player_id: The ID of the player to add
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.debug(f"Adding player {player_id} to team {team_id}")
            
            # Check if player and team exist
            team = session.query(TeamInSeries).get(team_id)
            player = session.query(Player).get(player_id)
            
            if not team or not player:
                self.logger.warning(f"Team {team_id} or player {player_id} not found")
                return False

            # Check if player is already in team
            existing = session.query(RosterPlayersInSeries).filter_by(
                registration_id=team_id,
                player_id=player_id
            ).first()

            if existing:
                self.logger.debug(f"Player {player_id} already in team {team_id}")
                return True

            # Add player to team
            roster_entry = RosterPlayersInSeries(
                registration_id=team_id,
                player_id=player_id
            )
            session.add(roster_entry)
            session.commit()
            
            self.logger.info(f"Successfully added player {player_id} to team {team_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding player to team: {e}", exc_info=True)
            session.rollback()
            return False

    def remove_player_from_team(self, session: Session, team_id: int, player_id: int) -> bool:
        """Remove a player from a team's roster"""
        try:
            self.logger.debug(f"Removing player {player_id} from team {team_id}")
            
            roster_entry = session.query(RosterPlayersInSeries).filter_by(
                registration_id=team_id,
                player_id=player_id
            ).first()

            if roster_entry:
                session.delete(roster_entry)
                session.commit()
                self.logger.info(f"Successfully removed player {player_id} from team {team_id}")
                return True
            
            self.logger.warning(f"Player {player_id} not found in team {team_id}")
            return False

        except Exception as e:
            self.logger.error(f"Error removing player from team: {e}", exc_info=True)
            session.rollback()
            return False

    def get_team_players(self, session: Session, team_id: int) -> list:
        """Get all players in a team"""
        try:
            players = session.query(Player)\
                .join(RosterPlayersInSeries)\
                .filter(RosterPlayersInSeries.registration_id == team_id)\
                .all()
            return players
        except Exception as e:
            self.logger.error(f"Error getting team players: {e}", exc_info=True)
            return []

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
