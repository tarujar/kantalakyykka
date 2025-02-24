from sqlalchemy.orm import Session
from app.models.models import ThrowType, SingleThrow, SingleRoundThrow
from app.utils.throw_input import ThrowInputField
import logging

class ThrowService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

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

    def save_round_throw(self, session: Session, game_id: int, game_set_index: int, throw_round: int,
                        is_home_team: bool, player_id: int, throws: list[str], team_id: int, 
                        existing_throw=None, player_position: int = 1):
        """Save a round of 2 consecutive throws for a player"""
        base_throw_index = self.calculate_throw_index(
            game_set_index, 
            throw_round, 
            is_home_team, 
            player_position
        )

        # Save the two individual throws
        throw_ids = []
        for i, throw_data in enumerate(throws):
            throw_index = base_throw_index + i
            existing_throw_id = getattr(existing_throw, f'throw_{i+1}') if existing_throw else None
            
            throw_id = self.save_throw(
                session,
                throw_data,
                player_id,
                throw_index,
                existing_throw_id
            )
            throw_ids.append(throw_id)

        # Create or update the round throw record
        if existing_throw:
            for i, throw_id in enumerate(throw_ids, 1):
                setattr(existing_throw, f'throw_{i}', throw_id)
        else:
            round_throw = SingleRoundThrow(
                game_id=game_id,
                game_set_index=game_set_index,
                throw_position=throw_round,
                home_team=is_home_team,
                team_id=team_id,
                throw_1=throw_ids[0],
                throw_2=throw_ids[1],
                throw_3=throw_ids[2],
                throw_4=throw_ids[3]
            )
            session.add(round_throw)
            
        return True

    def save_throw_round(self, session, game_id: int, round_number: int, throw_order: int, player_id: int, 
                        throws: list[str], is_home_team: bool, existing_throw=None):
        """Save a throw round (2 consecutive throws by one player)"""
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
        """Get the correct throw sequence based on game type and round number"""
        if game_type.team_size == 2:
            # 2-player team sequence repeats every 2 throws
            player_index = (round_number - 1) % 2
            return [
                {"order": 1, "player_index": player_index},
                {"order": 2, "player_index": (player_index + 1) % 2}
            ]
        elif game_type.team_size == 4:
            # 4-player team sequence repeats every 4 throws
            base_index = ((round_number - 1) * 2) % 4
            return [
                {"order": 1, "player_index": base_index},
                {"order": 2, "player_index": (base_index + 1) % 4}
            ]
        else:
            # Personal league - single player throws all
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
