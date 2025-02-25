import logging
from flask import flash
from app.utils.constants import FormDefaults

logger = logging.getLogger(__name__)

class GameFormHandler:
    def __init__(self, session, game_service):
        self.session = session
        self.game_service = game_service

    def get_player_choices(self, team1_id, team2_id, get_team_players_func):
        """Get player choices for both teams"""
        team1_players = get_team_players_func(team1_id, self.session) or FormDefaults.NO_PLAYERS_LIST
        team2_players = get_team_players_func(team2_id, self.session) or FormDefaults.NO_PLAYERS_LIST
        return team1_players, team2_players

    def save_form(self, game_id, form):
        """Save form data"""
        try:
            self.game_service.process_game_throws(game_id, form, self.session)
            flash('Throws saved successfully!', 'success')
            return True
        except Exception as e:
            logger.error(f"Error saving throws: {e}", exc_info=True)
            flash('Error saving throws', 'error')
            return False
