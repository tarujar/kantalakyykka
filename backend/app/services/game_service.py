from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from ..models.models import Game as GameModel, GameType as GameTypeModel, SingleRoundThrow
from ..models.schemas import GameCreate, Game
import logging
from app.services.throw_service import ThrowService

class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.throw_service = ThrowService()

    def process_game_throws(self, game_id, form, session):
        """Process throws for a game"""
        self.logger.debug(f"Processing throws for game {game_id}")

        # Initial rollback to ensure clean state
        session.rollback()
        
        try:
            # Update game scores first
            game = session.query(GameModel).get(game_id)
            if game:
                game.score_1_1 = form.score_1_1.data
                game.score_1_2 = form.score_1_2.data
                game.score_2_1 = form.score_2_1.data
                game.score_2_2 = form.score_2_2.data

            # Get existing throws for mapping
            existing_throws = session.query(SingleRoundThrow).filter_by(game_id=game_id).all()
            existing_throws_map = {(t.game_set_index, t.throw_position, t.home_team): t for t in existing_throws}
            
            # Process throws for each team
            for team_index, team_throws in enumerate([form.team_1_round_throws, form.team_2_round_throws]):
                is_home_team = team_index == 0
                for entry in team_throws:
                    for round_num in [1, 2]:
                        self._process_round_throws(session, game_id, entry, round_num, is_home_team, existing_throws_map)
            
            # Try to commit all changes
            session.commit()
            self.logger.info(f"Successfully saved all throws for game {game_id}")
            return True
            
        except Exception as e:
            # Error rollback
            self.logger.error(f"Error processing throws: {e}", exc_info=True)
            session.rollback()
            raise

    def _process_round_throws(self, session, game_id, entry, round_num, is_home_team, existing_throws_map):
        """Process throws for a single round"""
        round_data = getattr(entry, f'round_{round_num}')
        for pos, throw_form in enumerate(round_data, 1):
            existing_throw = existing_throws_map.get((round_num, pos, is_home_team))
            self.throw_service.save_round_throw(
                session,
                game_id=game_id,
                round_num=round_num,
                position=pos,
                is_home_team=is_home_team,
                player_id=throw_form.player_id.data,
                throws=[
                    throw_form.throw_1.data,
                    throw_form.throw_2.data,
                    throw_form.throw_3.data,
                    throw_form.throw_4.data
                ],
                existing_throw=existing_throw
            )

async def calculate_game_score(team_score: int, points_multiplier: int = 1) -> int:
    """Calculate game score with multiplier.
    
    Args:
        team_score: The raw score for the team
        points_multiplier: Score multiplier (1 for regular season, 2 for playoffs)
    
    Returns:
        int: Calculated score
        
    Raises:
        ValueError: If points_multiplier is not 1 or 2
    """
    if points_multiplier not in [1, 2]:
        raise ValueError("Points multiplier must be 1 (regular season) or 2 (playoffs)")
    return team_score * points_multiplier

async def create_game(db: AsyncSession, game: GameCreate) -> Game:
    await validate_game_players(db, game.game_type_id, game.players)
    db_game = GameModel(
        series_id=game.series_id,
        round=game.round,
        is_playoff=game.is_playoff,
        game_date=game.game_date,
        team_1_id=game.team_1_id,
        team_2_id=game.team_2_id,
        score_1_1=game.score_1_1,
        score_1_2=game.score_1_2,
        score_2_1=game.score_2_1,
        score_2_2=game.score_2_2,
    )
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def get_game(db: AsyncSession, game_id: int) -> Game:
    result = await db.execute(select(GameModel).filter(GameModel.id == game_id))
    db_game = result.scalars().first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

async def list_games(db: AsyncSession) -> list[GameModel]:
    result = await db.execute(select(GameModel))
    return result.scalars().all()

async def validate_game_players(db: AsyncSession, game_type_id: int, players: list[int]):
    result = await db.execute(select(GameTypeModel).filter(GameTypeModel.id == game_type_id))
    game_type = result.scalars().first()
    if not game_type:
        raise HTTPException(status_code=400, detail="Invalid game type")
    
    team_player_amount = game_type.team_player_amount
    if len(players) > team_player_amount:
        raise HTTPException(status_code=400, detail="Too many players for this game type")
    if len(players) < team_player_amount:
        raise HTTPException(status_code=400, detail="Not enough players for this game type")

async def update_game(db: AsyncSession, game_id: int, game: GameCreate) -> Game:
    db_game = await get_game(db, game_id)
    if db_game is None:
        return None
    for key, value in game.model_dump().items():
        setattr(db_game, key, value)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def delete_game(db: AsyncSession, game_id: int) -> bool:
    db_game = await get_game(db, game_id)
    if db_game is None:
        return False
    await db.delete(db_game)
    await db.commit()
    return True