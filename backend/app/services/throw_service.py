from sqlalchemy.orm import Session
from app.models.models import ThrowType, SingleThrow, SingleRoundThrow
from app.utils.game_utils import process_throw_data
import logging
from app.utils.throw_input import ThrowInputField

class ThrowService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_round_throw(self, session: Session, game_id: int, game_set_index: int, 
                        throw_round: int, is_home_team: bool, player_1_id: str, 
                        player_2_id: str, throws: list, team_id: int) -> bool:
        """
        Save all throws for a complete round (both players, 4 throws total)
        
        Args:
            session: Database session
            game_id: Game ID
            game_set_index: Set number (1 or 2)
            throw_round: Round number within the set
            is_home_team: Whether this is home team
            player_1_id: ID of first player
            player_2_id: ID of second player
            throws: List of 4 throw values
            team_id: Team ID
        """
        try:
            # Get or create round throw record
            round_throw = self._get_or_create_round_throw(
                session, game_id, game_set_index, throw_round, is_home_team, team_id
            )

            # Process throws for both players
            throw_ids = []
            for i, (player_id, throws_pair) in enumerate([
                (int(player_1_id), throws[0:2]),
                (int(player_2_id), throws[2:4])
            ]):
                for j, throw in enumerate(throws_pair):
                    throw_index = throw_round * 4 - (3 - (i * 2 + j))
                    throw_id = self._save_single_throw(session, throw, player_id, throw_index)
                    throw_ids.append(throw_id)

            # Update round throw record with new throw IDs
            round_throw.throw_1, round_throw.throw_2, round_throw.throw_3, round_throw.throw_4 = throw_ids
            session.add(round_throw)
            session.flush()

            return True

        except Exception as e:
            self.logger.error(f"Error saving round throw: {e}", exc_info=True)
            raise

    def _get_or_create_round_throw(self, session: Session, game_id: int, game_set_index: int,
                                 throw_round: int, is_home_team: bool, team_id: int) -> SingleRoundThrow:
        """Get existing round throw record or create new one"""
        round_throw = session.query(SingleRoundThrow).filter_by(
            game_id=game_id,
            game_set_index=game_set_index,
            throw_position=throw_round,
            home_team=is_home_team
        ).first()

        if not round_throw:
            round_throw = SingleRoundThrow(
                game_id=game_id,
                game_set_index=game_set_index,
                throw_position=throw_round,
                home_team=is_home_team,
                team_id=team_id
            )

        return round_throw

    def _save_single_throw(self, session: Session, throw_data, player_id: int, throw_index: int) -> int:
        """Process and save a single throw, return its ID"""
        try:
            throw_type, throw_score = process_throw_data(str(throw_data))
            throw = SingleThrow(
                throw_type=throw_type,
                throw_score=throw_score,
                player_id=player_id,
                throw_index=throw_index
            )
            
            session.add(throw)
            session.flush()
            
            self.logger.debug(f"Saved throw: player={player_id}, type={throw.throw_type}, score={throw.throw_score}, index={throw_index}")
            return throw.id

        except Exception as e:
            self.logger.error(f"Error saving single throw: {e}", exc_info=True)
            raise

    def _parse_throw_string(self, value: str):
        """Parse throw string input and return (throw_type, throw_score)"""
        value = value.strip().upper()
        if value in ['H', 'F', 'E', '']:
            return {
                'H': (ThrowType.HAUKI, 0),
                'F': (ThrowType.FAULT, 0),
                'E': (ThrowType.E, 1),
                '': (ThrowType.E, 1)
            }[value]
        
        try:
            score = int(value)
            if -40 <= score <= 80:
                return (ThrowType.VALID, score)
        except ValueError:
            pass
        
        raise ValueError(f"Invalid throw value: {value}")

    def save_throw(self, session: Session, throw_data, player_id: int, throw_index: int, existing_throw_id=None) -> int:
        """Save a single throw and return its ID"""
        if not throw_data:
            return None

        throw_type_value, throw_score_value = self._process_throw_data(throw_data)
        if throw_type_value is None:
            return None

        throw = self._get_or_create_throw(
            session, 
            throw_type_value, 
            throw_score_value, 
            player_id,
            throw_index,
            existing_throw_id
        )
        
        session.add(throw)
        session.flush()
        return throw.id

    def calculate_throw_index(self, game_set_index: int, throw_round: int, is_home_team: bool, player_position: int) -> int:
        """Calculate the global throw index (1-20) based on set, round, team and player position"""
        # Each throw round has 8 throws (4 per team)
        throws_per_round = 8
        # Calculate base index for the set and round
        base_index = ((game_set_index - 1) * throw_round * throws_per_round) + \
                    ((throw_round - 1) * throws_per_round)
        
        # Add team offset (0 for home team, 4 for away team)
        team_offset = 4 if not is_home_team else 0
        
        # Add player position offset (0 for first player, 2 for second player)
        player_offset = 2 * (player_position - 1)
        
        # Final index is base + team offset + player offset + 1
        return base_index + team_offset + player_offset + 1

    def get_player_for_round(self, throw_round: int, player_position: int, total_players: int) -> int:
        """Get the player index (0-based) for the current round and position
        
        Args:
            throw_round: Current throw round (1-based)
            player_position: Position in the round (1 for first player, 2 for second player)
            total_players: Total number of players in team
        
        Returns:
            0-based index of the player who should throw
        """
        # In a 4-player game:
        # Round 1: Players 0,1 throw
        # Round 2: Players 2,3 throw
        # Round 3: Players 0,1 throw again
        # Round 4: Players 2,3 throw again
        base_player = (((throw_round - 1) // 2) * 2) % total_players
        return (base_player + player_position - 1) % total_players

    def save_throw_round(self, session, game_id: int, round_number: int, throw_order: int, 
                        player_id: int, throws: list[str], is_home_team: bool, 
                        existing_throw=None):
        """Save or update a throw round record"""
        if existing_throw:
            existing_throw.throw_1 = throws[0]
            existing_throw.throw_2 = throws[1]
            existing_throw.player_id = player_id
        else:
            new_throw = SingleRoundThrow(
                game_id=game_id,
                round_number=round_number,
                throw_order=throw_order,
                player_id=player_id,
                throw_1=throws[0],
                throw_2=throws[1],
                throw_3=throws[2],
                throw_4=throws[3],
                is_home_team=is_home_team
            )
            session.add(new_throw)

    def get_throw_sequence(self, game_type, round_number: int, is_home_team: bool) -> list[dict]:
        """Get the throwing sequence based on game type and round number"""
        # Map team sizes to their sequence logic
        sequence_handlers = {
            2: self._get_two_player_sequence,
            4: self._get_four_player_sequence
        }
        
        handler = sequence_handlers.get(game_type.team_size, self._get_personal_sequence)
        return handler(round_number)

    def _get_two_player_sequence(self, round_number: int) -> list[dict]:
        player_index = (round_number - 1) % 2
        return [
            {"order": 1, "player_index": player_index},
            {"order": 2, "player_index": (player_index + 1) % 2}
        ]

    def _get_four_player_sequence(self, round_number: int) -> list[dict]:
        base_index = ((round_number - 1) * 2) % 4
        return [
            {"order": 1, "player_index": base_index},
            {"order": 2, "player_index": (base_index + 1) % 4}
        ]

    def _get_personal_sequence(self, round_number: int) -> list[dict]:
        return [{"order": 1, "player_index": 0}]

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

    def _get_or_create_throw(self, session, throw_type_value, throw_score_value, player_id, throw_index, existing_throw_id):
        """Get existing throw or create new one"""
        if existing_throw_id:
            throw = session.query(SingleThrow).get(existing_throw_id)
            if throw:
                throw.throw_type = throw_type_value
                throw.throw_score = throw_score_value
                throw.player_id = player_id
                throw.throw_index = throw_index
                return throw
        return SingleThrow(
            throw_type=throw_type_value,
            throw_score=throw_score_value,
            player_id=player_id,
            throw_index=throw_index
        )
