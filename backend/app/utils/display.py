from app.models import SeriesRegistration, Series, Player  # Changed from SeriesRegistration
from flask_babel import gettext as _
from app.main import app
import logging

def format_player_name(session, player_id):
    """Format player name for display in admin views"""
    if player_id:
        player = session.query(Player).get(player_id)
        return player.name if player else str(player_id)
    return ''

def format_series_name(session, series_id):
    """Format series name for display in admin views"""
    if series_id:
        series = session.query(Series).get(series_id)
        return f"{series.name} ({series.year})" if series else str(series_id)
    return ''

def format_team_name(session, team_id):
    """Format team name for display in admin views"""
    if not team_id:
        return ""
    reg = session.query(SeriesRegistration).get(team_id)  # Changed from TeamInSeries
    if reg:
        return f"{reg.team_name} ({reg.team_abbreviation})" if reg.team_name else reg.contact_player.name
    return ""

def format_player_contact_info(session, player_id):
    """Format player name and email for display in admin views"""
    if player_id:
        player = session.query(Player).get(player_id)
        return f"{player.name} ({player.email})" if player else str(player_id)
    return ''

def format_end_game_score(model):
    """Format end game score for display in admin views"""
    team_1_score = model.score_1_1 + model.score_1_2
    team_2_score = model.score_2_1 + model.score_2_2
    return f"{team_1_score} - {team_2_score}"

def custom_gettext(key):
    try:
        with app.app_context():
            translation = str(_(key))
            logging.info(f"Translation attempt - Key: '{key}', Result: '{translation}'")
            return translation
    except Exception as e:
        logging.error(f"Translation error for key '{key}': {e}")
        return key

logging.info("Translation files loaded successfully")
