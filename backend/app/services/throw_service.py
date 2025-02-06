from sqlalchemy.orm import Session
from app.models.models import ThrowType, SingleThrow, SingleRoundThrow
from app.utils.throw_input import ThrowInputField
import logging

class ThrowService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_throw(self, session: Session, throw_data, existing_throw_id=None) -> int:
        """Save a single throw and return its ID"""
        if not throw_data:
            return None

        throw_type_value, throw_score_value = self._process_throw_data(throw_data)
        if throw_type_value is None:
            return None

        throw = self._get_or_create_throw(session, throw_type_value, throw_score_value, existing_throw_id)
        if not throw:
            return None

        session.add(throw)
        session.flush()
        return throw.id

    def save_round_throw(self, session: Session, game_id: int, round_num: int, position: int, 
                        is_home_team: bool, player_id: str, throws: list, existing_throw=None):
        """Save or update a round of throws (4 throws) for a player
        Args:
            session: Database session
            game_id: ID of the game
            round_num: Round number (1 or 2)
            position: Position in the round (1-5)
            is_home_team: Whether this is for the home team
            player_id: ID of the player making the throws
            throws: List of 4 throw values
            existing_throw: Existing SingleRoundThrow record if updating
        """
        self.logger.debug(f"Saving round throw: round={round_num}, pos={position}, home={is_home_team}")
        
        # Save individual throws first
        throw_ids = []
        for i, throw_data in enumerate(throws):
            existing_throw_id = getattr(existing_throw, f'throw_{i+1}') if existing_throw else None
            throw_id = self.save_throw(session, throw_data, existing_throw_id)
            throw_ids.append(throw_id)
            self.logger.debug(f"Saved throw {i+1}: {throw_id}")

        if existing_throw:
            # Update existing round throw
            existing_throw.player_id = player_id
            for i, throw_id in enumerate(throw_ids, 1):
                setattr(existing_throw, f'throw_{i}', throw_id)
            self.logger.debug(f"Updated existing round throw: {existing_throw.id}")
        else:
            # Create new round throw
            round_throw = SingleRoundThrow(
                game_id=game_id,
                game_set_index=round_num,
                throw_position=position,
                home_team=is_home_team,
                player_id=player_id,
                throw_1=throw_ids[0],
                throw_2=throw_ids[1],
                throw_3=throw_ids[2],
                throw_4=throw_ids[3]
            )
            session.add(round_throw)
            session.flush()
            self.logger.debug(f"Created new round throw: {round_throw.id}")

        return True

    def _process_throw_data(self, throw_data):
        """Process throw data and return (throw_type, throw_score)"""
        if isinstance(throw_data, str):
            return self._process_string_throw(throw_data)
        elif isinstance(throw_data, (int, float)):
            return self._process_numeric_throw(throw_data)
        elif isinstance(throw_data, ThrowInputField):
            return throw_data.throw_type.data, throw_data.throw_score.data
        return None, None

    def _process_string_throw(self, value):
        """Process string throw input"""
        value = value.strip().upper()
        if value in ['H', 'F', 'E', '']:
            switcher = {
                'H': (ThrowType.HAUKI.value, 0),
                'F': (ThrowType.FAULT.value, 0),
                'E': (ThrowType.E.value, 1),
                '': (ThrowType.E.value, 1)
            }
            return switcher[value]
        try:
            score = int(value)
            if -40 <= score <= 80:
                return ThrowType.VALID.value, score
        except ValueError:
            pass
        return None, None

    def _process_numeric_throw(self, value):
        """Process numeric throw input"""
        if -40 <= value <= 80:
            return ThrowType.VALID.value, value
        return None, None

    def _get_or_create_throw(self, session, throw_type_value, throw_score_value, existing_throw_id):
        """Get existing throw or create new one"""
        if existing_throw_id:
            throw = session.query(SingleThrow).get(existing_throw_id)
            if throw:
                throw.throw_type = throw_type_value
                throw.throw_score = throw_score_value
                return throw
        return SingleThrow(
            throw_type=throw_type_value,
            throw_score=throw_score_value
        )
