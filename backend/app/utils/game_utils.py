from app.models.models import SingleRoundThrow, SingleThrow, ThrowType
from app.utils.throw_input import ThrowInputField
import logging
from wtforms import StringField

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def set_player_choices(form, team1_players, team2_players):
    """Set player choices for both players in each round"""
    if not form or not hasattr(form, 'team_1_round_throws'):
        logger.error("Invalid form structure")
        return

    # Get game type from the form
    game_type = getattr(form, 'game_type', None)
    if not game_type:
        logger.error("Game type not found in form")
        return

    throw_round_amount = game_type.throw_round_amount

    # For team 1
    for entry in form.team_1_round_throws:
        entry.game_type = game_type  # Set game_type for the entry
        for round_num in range(1, throw_round_amount + 1):
            round_field = entry.get_round(round_num)
            if round_field and hasattr(round_field.form, 'player_1_id'):
                round_field.form.player_1_id.choices = [('-1', '-- Select Player 1 --')] + team1_players
                round_field.form.player_2_id.choices = [('-1', '-- Select Player 2 --')] + team1_players
                logger.debug(f"Set team 1 player choices for round {round_num}")

    # For team 2
    for entry in form.team_2_round_throws:
        entry.game_type = game_type  # Set game_type for the entry
        for round_num in range(1, throw_round_amount + 1):
            round_field = entry.get_round(round_num)
            if round_field and hasattr(round_field.form, 'player_1_id'):
                round_field.form.player_1_id.choices = [('-1', '-- Select Player 1 --')] + team2_players
                round_field.form.player_2_id.choices = [('-1', '-- Select Player 2 --')] + team2_players
                logger.debug(f"Set team 2 player choices for round {round_num}")

def set_throw_value(throw_form, throw, throw_number):
    """Set throw value and log warning if throw is not found"""
    if throw:
        setattr(throw_form, f'throw_{throw_number}', ThrowInputField.get_throw_value(throw))
    else:
        logger.warning(f"Throw {throw_number} not found for throw ID {getattr(throw, f'throw_{throw_number}') if throw else 'N/A'}")

def _create_form_field_name(set_index, round_num, team_num, field_type, number=None):
    """Create standardized form field name"""
    base = f"set_{set_index}_round_{round_num}_team_{team_num}_{field_type}"
    return f"{base}_{number}" if number is not None else base

def _add_field_if_missing(form, field_name, field_type=StringField):
    """Add a field to the form if it doesn't exist"""
    if not hasattr(form, field_name):
        setattr(form, field_name, field_type())
        if not hasattr(form, '_fields'):
            form._fields = {}
        form._fields[field_name] = getattr(form, field_name)

def load_existing_throws(session, form, game):
    """Load existing throws into form"""
    throws = session.query(SingleRoundThrow).filter_by(game_id=game.id).all()
    logger.debug(f"Loading throws for game {game.id}: found {len(throws)} throws")

    # First load game scores
    form.score_1_1.data = game.score_1_1
    form.score_1_2.data = game.score_1_2
    form.score_2_1.data = game.score_2_1
    form.score_2_2.data = game.score_2_2

    # Then load throws
    for throw in throws:
        try:
            # Determine prefix
            team_num = 1 if throw.home_team else 2
            set_index = throw.game_set_index
            round_num = throw.throw_position

            # Create fields for this round if they don't exist
            for field_type in ['player', 'throw']:
                for num in range(1, 5):
                    field_name = _create_form_field_name(set_index, round_num, team_num, field_type, num)
                    _add_field_if_missing(form, field_name)
                    logger.debug(f"Ensured field exists: {field_name}")

            # Load player IDs
            if throw.throw_1:
                player1 = session.query(SingleThrow).get(throw.throw_1)
                if player1:
                    field_name = _create_form_field_name(set_index, round_num, team_num, 'player', 1)
                    form._fields[field_name].data = str(player1.player_id)
                    logger.debug(f"Set {field_name}={player1.player_id}")

            if throw.throw_3:
                player2 = session.query(SingleThrow).get(throw.throw_3)
                if player2:
                    field_name = _create_form_field_name(set_index, round_num, team_num, 'player', 2)
                    form._fields[field_name].data = str(player2.player_id)
                    logger.debug(f"Set {field_name}={player2.player_id}")

            # Load throws
            throws_map = {
                1: throw.throw_1,
                2: throw.throw_2,
                3: throw.throw_3,
                4: throw.throw_4
            }

            for throw_num, throw_id in throws_map.items():
                if throw_id:
                    single_throw = session.query(SingleThrow).get(throw_id)
                    if single_throw:
                        field_name = _create_form_field_name(set_index, round_num, team_num, 'throw', throw_num)
                        
                        # Convert throw to display format
                        value = {
                            ThrowType.VALID: str(single_throw.throw_score),
                            ThrowType.HAUKI: 'H',
                            ThrowType.FAULT: 'F',
                            ThrowType.E: 'E'
                        }.get(single_throw.throw_type, 'E')
                        
                        form._fields[field_name].data = value
                        logger.debug(f"Set {field_name}={value}")

        except Exception as e:
            logger.error(f"Error loading throw data: {e}", exc_info=True)
            continue

import logging
from app.models.models import ThrowType

logger = logging.getLogger(__name__)

def process_throw_data(throw_data):
    """Process individual throw data"""
    if not throw_data:
        return None, 0

    value = str(throw_data).strip().upper()
    
    # Handle special throw types
    if value in ['H', 'F', 'E', '']:
        return {
            'H': ('HAUKI', 0),
            'F': ('FAULT', 0),
            'E': ('E', 1),
            '': ('E', 1)
        }[value]

    # Handle numeric scores
    try:
        score = int(value)
        if -40 <= score <= 80:
            return 'VALID', score
        logger.error(f"Invalid score value: {score}")
    except ValueError:
        logger.error(f"Invalid throw value: {value}")
    
    return None, 0

def process_game_scores(game, form_data):
    """Process and update game scores from form data"""
    game.score_1_1 = int(form_data.get('score_1_1', 0))
    game.score_1_2 = int(form_data.get('score_1_2', 0))
    game.score_2_1 = int(form_data.get('score_2_1', 0))
    game.score_2_2 = int(form_data.get('score_2_2', 0))
    return game
