from app.models.models import SingleRoundThrow, SingleThrow
from app.utils.throw_input import ThrowInputField
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def process_single_throw(session, game_service, game_id, throw_form, round_num, pos, is_home_team, existing_throws_map):
    """Helper method to process a single throw"""
    logger.debug(f"Processing throw for round {round_num}, position {pos}, home_team {is_home_team}")
    
    # Check if this throw already exists
    existing_throw = existing_throws_map.get((round_num, pos, is_home_team))
    
    # Save each throw and get its ID
    throw_1_id = game_service.save_throw(session, throw_form.throw_1, existing_throw.throw_1 if existing_throw else None)
    throw_2_id = game_service.save_throw(session, throw_form.throw_2, existing_throw.throw_2 if existing_throw else None)
    throw_3_id = game_service.save_throw(session, throw_form.throw_3, existing_throw.throw_3 if existing_throw else None)
    throw_4_id = game_service.save_throw(session, throw_form.throw_4, existing_throw.throw_4 if existing_throw else None)
    session.flush()  # Ensure throw IDs are available
    
    player_id = throw_form.player_id.data  # Extract the player_id value

    if existing_throw:
        # Update existing throw
        existing_throw.player_id = player_id
        existing_throw.throw_1 = throw_1_id
        existing_throw.throw_2 = throw_2_id
        existing_throw.throw_3 = throw_3_id
        existing_throw.throw_4 = throw_4_id
        logger.debug(f"Updated existing throw: {existing_throw.__dict__}")
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
        logger.debug(f"New throw saved with ID: {throw.id}")

def set_player_choices(form, team1_players, team2_players):
    """Set player choices for form fields"""
    for team_index, (throws, players) in enumerate([(form.team_1_round_throws, team1_players), 
                                                  (form.team_2_round_throws, team2_players)]):
        for entry in throws.entries:
            for round_num in [1, 2]:
                for throw_form in entry[f'round_{round_num}'].entries:
                    throw_form.player_id.choices = players
                    throw_form.home_team.data = (team_index == 0)  # Set home_team flag based on team index

def set_throw_value(throw_form, throw, throw_number):
    """Set throw value and log warning if throw is not found"""
    if throw:
        setattr(throw_form, f'throw_{throw_number}', ThrowInputField.get_throw_value(throw))
    else:
        logger.warning(f"Throw {throw_number} not found for throw ID {getattr(throw, f'throw_{throw_number}') if throw else 'N/A'}")

def load_existing_throws(session, form, game):
    """Load existing throws into form"""
    throws = session.query(SingleRoundThrow).filter_by(game_id=game.id).all()

    if not throws:
        return

    # Load round scores from the games table
    form.score_1_1.data = game.score_1_1
    form.score_1_2.data = game.score_1_2
    form.score_2_1.data = game.score_2_1
    form.score_2_2.data = game.score_2_2

    # Calculate end scores
    form.end_score_team_1.data = game.score_1_1 + game.score_1_2
    form.end_score_team_2.data = game.score_2_1 + game.score_2_2

    for throw in throws:
        team_field = form.team_1_round_throws if throw.home_team else form.team_2_round_throws
        try:
            throw_form = team_field.entries[0][f'round_{throw.game_set_index}'].entries[throw.throw_position - 1]
            throw_form.player_id.data = str(throw.player_id)  # Ensure player_id is set as a string

            # Set throw values using the helper function
            set_throw_value(throw_form, throw.throw_1, 1)
            set_throw_value(throw_form, throw.throw_2, 2)
            set_throw_value(throw_form, throw.throw_3, 3)
            set_throw_value(throw_form, throw.throw_4, 4)

        except (IndexError, AttributeError) as e:
            logger.error(f"Error mapping throws: {e}")
