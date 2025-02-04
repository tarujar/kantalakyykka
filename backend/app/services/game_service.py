from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from ..models.models import Game as GameModel, GameType as GameTypeModel
from ..models.schemas import GameCreate, Game

import logging
from app.models.models import ThrowType, Game, SingleRoundThrow, SingleThrow
from sqlalchemy.orm import Session
from app.utils.throw_input import convert_throw_type_to_str

class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def save_throw(self, session: Session, throw_form_field, existing_throw_id=None) -> int:
        """Save a single throw and return its ID
        Args:
            session: SQLAlchemy session
            throw_form_field: ThrowInputField instance with throw_type and throw_score
            existing_throw_id: ID of the existing throw to update, if any
        Returns:
            int: ID of created or updated SingleThrow record or None if no throw
        """
        if not throw_form_field or not hasattr(throw_form_field, 'data'):
            self.logger.debug(f"Throw form field is missing or invalid {throw_form_field.__dict__}" )
            return None
        self.logger.debug(f"SAVETHROW exist: {existing_throw_id}, {throw_form_field.throw_type}, {throw_form_field.throw_score}" )
    
        if throw_form_field.throw_type in [ThrowType.HAUKI.value, ThrowType.FAULT.value, ThrowType.VALID.value, ThrowType.E.value]:

            if existing_throw_id:
                throw = session.query(SingleThrow).get(existing_throw_id)
                if throw:
                    throw.throw_type = convert_throw_type_to_str(throw_form_field.throw_type)
                    throw.throw_score = throw_form_field.throw_score
                    self.logger.debug(f"Updated throw: {throw.__dict__}")
                else:
                    self.logger.warning(f"Existing throw with ID {existing_throw_id} not found")
                    throw = SingleThrow(
                        throw_type=convert_throw_type_to_str(throw_form_field.throw_type),
                        throw_score=throw_form_field.throw_score
                    )
                    session.add(throw)
                    session.flush()  # Get the ID without committing
                    self.logger.debug(f"Saved new throw: {throw.__dict__}")
            else:
                throw = SingleThrow(
                    throw_type=convert_throw_type_to_str(throw_form_field.throw_type),
                    throw_score=throw_form_field.throw_score
                )
                session.add(throw)
                session.flush()  # Get the ID without committing
                self.logger.debug(f"Saved new throw: {throw.__dict__}")

            return throw.id
        else:
            self.logger.debug(f"Invalid throw form field data: {throw_form_field}")
            return None

    def process_game_throws(self, game_id, form, session):
        """Process throws for a game"""
        try:
            # Start fresh - rollback any existing transaction
            session.rollback()
            
            # Get existing throws
            existing_throws = session.query(SingleRoundThrow).filter_by(game_id=game_id).all()
            existing_throws_map = {(t.game_set_index, t.throw_position, t.home_team): t for t in existing_throws}
            
            # Process new throws
            for team_index, team_throws in enumerate([form.team_1_round_throws, form.team_2_round_throws]):
                is_home_team = team_index == 0
                team_name = "Team 1" if is_home_team else "Team 2"
                self.logger.debug(f"Processing throws for {team_name}")
                
                for entry in team_throws:
                    for round_num in [1, 2]:
                        round_data = getattr(entry, f'round_{round_num}')
                        for pos, throw_form in enumerate(round_data, 1):
                            self.logger.debug(f"Throw {round_num} {throw_form.__dict__}")
                            
                            # Check if this throw already exists
                            existing_throw = existing_throws_map.get((round_num, pos, is_home_team))
                            
                            # Save each throw and get its ID
                            throw_1_id = self.save_throw(session, throw_form.throw_1, existing_throw.throw_1 if existing_throw else None)
                            throw_2_id = self.save_throw(session, throw_form.throw_2, existing_throw.throw_2 if existing_throw else None)
                            throw_3_id = self.save_throw(session, throw_form.throw_3, existing_throw.throw_3 if existing_throw else None)
                            throw_4_id = self.save_throw(session, throw_form.throw_4, existing_throw.throw_4 if existing_throw else None)
                            session.flush()  # Ensure throw IDs are available
                            
                            player_id = throw_form.player_id.data  # Extract the player_id value

                            if existing_throw:
                                # Update existing throw
                                existing_throw.player_id = player_id
                                existing_throw.throw_1 = throw_1_id
                                existing_throw.throw_2 = throw_2_id
                                existing_throw.throw_3 = throw_3_id
                                existing_throw.throw_4 = throw_4_id
                                self.logger.debug(f"Updated existing throw: {existing_throw.__dict__}")
                            else:
                                # Create new throw
                                throw = SingleRoundThrow(
                                    game_id=game_id,
                                    game_set_index=round_num,
                                    throw_position=pos,
                                    home_team=is_home_team,
                                    player_id=player_id,
                                    throw_1=throw_1_id,
                                    throw_2=throw_2_id,
                                    throw_3=throw_3_id,
                                    throw_4=throw_4_id
                                )
                                session.add(throw)
                                session.flush()
                                self.logger.debug(f"New throw saved with ID: {throw.id}")
            
            # Commit all changes
            session.commit()
            self.logger.info("Successfully saved all throws")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing throws: {e}", exc_info=True)
            session.rollback()
            raise

    def get_throws_by_type(self, session: Session, throw_type: ThrowType):
        """Get all throws of a specific type"""
        return session.query(SingleThrow).filter(SingleThrow.throw_type == throw_type.value).all()

async def calculate_game_score(team_score: int, points_multiplier: int) -> int:
    if points_multiplier not in [1, 2]:
        raise ValueError("Invalid season")
    return team_score * points_multiplier 

def calculate_throw_points(throw_input: str) -> tuple[int, str | None]:
    """Laskee heiton pisteet ja tyypin syötteen perusteella.
    
    Sallitut syötteet:
    - Numero väliltä -8..80: suora pistemäärä
    - H: hauki (ei osumaa, 0 pistettä)
    - -: hylätty (0 pistettä)
    - U: käyttämätön (0 pistettä)
    """
    match throw_input:
        case 'H':
            return (0, 'H')      # Ei osumaa
        case '-':
            return (0, '-')      # Hylätty
        case 'U':
            return (0, 'U')      # Käyttämätön
        case _:
            try:
                points = int(throw_input)
                if -8 <= points <= 80:  # Sallittu pistemäärä
                    return (points, None)
                raise ValueError("Points must be between -8 and 80")
            except ValueError:
                raise ValueError(f"Invalid throw input: {throw_input}")

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
    
    max_players = game_type.max_players
    if len(players) > max_players:
        raise HTTPException(status_code=400, detail="Too many players for this game type")
    if len(players) < max_players:
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