from app.main import db, app
from app.models.models import GameType, Series, Player, TeamInSeries, RosterPlayersInSeries
from flask import current_app

def get_game_type_choices():
    with app.app_context():
        choices = [(str(gt.id), gt.name) for gt in db.session.query(GameType).all()]
        default = next((str(gt.id) for gt in db.session.query(GameType).all() if gt.name == "Joukkue"), None)
    return choices, default

def get_series_choices():
    """Returns a list of tuples containing (id, name, year) for all series with open registration"""
    with app.app_context():
        series_list = db.session.query(Series).filter(Series.registration_open == True).all()
        choices = [(str(s.id), s.name, s.year) for s in series_list]
        default = choices[0][0] if choices else None
        return choices, default

def get_player_choices():
    """Returns a list of tuples containing (id, display_name, email) for all players"""
    with current_app.app_context():
        players = db.session.query(Player).all()
        return [(player.id, player.name, player.email) for player in players]

def get_player_choices_for_form():
    """Returns a list of tuples containing (id, name) for all players"""
    with current_app.app_context():
        players = db.session.query(Player).all()
        return [(player.id, player.name) for player in players]

def get_team_choices_by_series():
    with current_app.app_context():
        # Get all teams with their series, ordered appropriately
        teams = db.session.query(TeamInSeries, Series)\
                  .join(Series, TeamInSeries.series_id == Series.id)\
                  .order_by(Series.year.desc(), Series.name, TeamInSeries.team_name)\
                  .all()
        
        # Group teams by series
        series_groups = {}
        for team, series in teams:
            series_key = f"{series.name} {series.year}"
            if series_key not in series_groups:
                series_groups[series_key] = []
            series_groups[series_key].append(
                (str(team.id), f"{team.team_name} ({team.team_abbreviation})")
            )
        
        # Convert to list of tuples for optgroup structure
        return [
            (series_name, team_choices)
            for series_name, team_choices in series_groups.items()
        ]

def get_flat_team_choices():
    with current_app.app_context():
        # Get all teams with their series, ordered appropriately
        teams = db.session.query(TeamInSeries, Series)\
                  .join(Series, TeamInSeries.series_id == Series.id)\
                  .order_by(Series.year.desc(), Series.name, TeamInSeries.team_name)\
                  .all()
        
        # Create a flat list of tuples for team choices
        team_choices = [
            (team.id, f"{team.team_name} ({team.team_abbreviation})")
            for team, series in teams
        ]
        
        return team_choices

def get_team_choices_with_player_count():
    with current_app.app_context():
        team_choices = get_team_choices_by_series()
        choices_with_count = []
        for series_name, team_list in team_choices:
            updated_team_list = []
            for team_id, team_name in team_list:
                player_count = db.session.query(RosterPlayersInSeries).filter_by(registration_id=team_id).count()
                max_players = db.session.query(TeamInSeries).filter_by(id=team_id).first().series.game_type.max_players
                updated_team_list.append((team_id, f"{team_name} ({player_count}/{max_players})"))
            choices_with_count.append((series_name, updated_team_list))
        return choices_with_count

def get_team_choices_with_context():
    with current_app.app_context():
        return get_flat_team_choices()
