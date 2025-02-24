from sqlalchemy.orm import Session
from flask import request
from ..models.models import Game as GameModel, SingleRoundThrow
import logging
from app.services.throw_service import ThrowService

class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.throw_service = ThrowService()

    def process_game_throws(self, game_id: int, form, session: Session):
        """Process and save throws for both teams"""
        game = session.query(GameModel).get(game_id)
        if not game:
            raise ValueError("Game not found")

        self.logger.debug(f"Processing game throws for game {game_id}")
        
        try:
            # Update game scores
            game.score_1_1 = form.score_1_1.data
            game.score_1_2 = form.score_1_2.data
            game.score_2_1 = form.score_2_1.data
            game.score_2_2 = form.score_2_2.data

            # Get form data
            form_data = request.form
            
            # Process throws for both sets
            for set_index in [1, 2]:
                for round_num in range(1, game.series.game_type.throw_round_amount + 1):
                    for team_num, is_home_team in [(1, True), (2, False)]:
                        team_id = game.team_1_id if is_home_team else game.team_2_id
                        prefix = f"set_{set_index}_round_{round_num}_team_{team_num}"
                        
                        # Get player IDs
                        player_1_id = form_data.get(f"{prefix}_player_1")
                        player_2_id = form_data.get(f"{prefix}_player_2")
                        
                        # Get throws
                        throws = [form_data.get(f"{prefix}_throw_{i}") for i in range(1, 5)]

                        # Only save if we have all required data
                        if all(throws) and player_1_id and player_2_id:
                            self.logger.debug(f"Saving throws for {prefix}: p1={player_1_id}, p2={player_2_id}, throws={throws}")
                            
                            self.throw_service.save_round_throw(
                                session=session,
                                game_id=game.id,
                                game_set_index=set_index,
                                throw_round=round_num,
                                is_home_team=is_home_team,
                                team_id=team_id,
                                player_1_id=player_1_id,
                                player_2_id=player_2_id,
                                throws=throws
                            )

            session.commit()
            self.logger.debug("Successfully saved all throws and scores")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving throws: {e}", exc_info=True)
            raise

    def get_game(self, session: Session, game_id: int) -> GameModel:
        """Get a game by its ID"""
        return session.query(GameModel).get(game_id)

    def _get_player_data(self, team_data, set_index, throw_position):
        """Helper method to get correct player data from form structure"""
        try:
            round_data = team_data[0][f'round_{set_index}']
            return round_data[throw_position - 1]
        except (IndexError, KeyError):
            return None

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

    def calculate_game_score(self, team_score: int, points_multiplier: int = 1) -> int:
        """Calculate game score with multiplier."""
        if points_multiplier not in [1, 2]:
            raise ValueError("Points multiplier must be 1 (regular season) or 2 (playoffs)")
        return team_score * points_multiplier