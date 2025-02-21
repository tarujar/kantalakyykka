from app.main import db, app
from app.models.models import GameType, Series, Player, SeriesRegistration, RosterPlayersInSeries
from flask import current_app
import logging

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

def get_player_choices_with_contact():
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
        # Get all registrations with their series, ordered appropriately
        registrations = db.session.query(SeriesRegistration, Series)\
                  .join(Series, SeriesRegistration.series_id == Series.id)\
                  .filter(SeriesRegistration.team_name.isnot(None))\
                  .order_by(Series.year.desc(), Series.name, SeriesRegistration.team_name)\
                  .all()
        
        # Group teams by series
        series_groups = {}
        for reg, series in registrations:
            series_key = f"{series.name} {series.year}"
            if series_key not in series_groups:
                series_groups[series_key] = []
            series_groups[series_key].append(
                (str(reg.id), f"{reg.team_name} ({reg.team_abbreviation})")
            )
        
        return [(series_name, team_choices)
                for series_name, team_choices in series_groups.items()]

def get_flat_team_choices():
    with current_app.app_context():
        # Get all teams with their series, ordered appropriately
        teams = db.session.query(SeriesRegistration, Series)\
                  .join(Series, SeriesRegistration.series_id == Series.id)\
                  .order_by(Series.year.desc(), Series.name, SeriesRegistration.team_name)\
                  .all()
        
        # Create a flat list of tuples for team choices
        team_choices = [
            (team.id, f"{team.team_name} ({team.team_abbreviation})")
            for team, series in teams
        ]
        
        return team_choices

def get_team_choices_with_player_count():
    with current_app.app_context():
        # Get all registrations grouped by series
        registrations = db.session.query(SeriesRegistration)\
            .join(Series)\
            .filter(SeriesRegistration.team_name.isnot(None))\
            .order_by(Series.year.desc(), Series.name, SeriesRegistration.team_name)\
            .all()

        # Group by series
        series_groups = {}
        for reg in registrations:
            series_key = f"{reg.series.name} {reg.series.year}"
            if series_key not in series_groups:
                series_groups[series_key] = []
            
            # Get player count for this registration
            player_count = db.session.query(RosterPlayersInSeries)\
                .filter_by(registration_id=reg.id).count()
            # Get team_player_amount from the series game type
            team_player_amount = reg.series.game_type.team_player_amount
            
            series_groups[series_key].append(
                (str(reg.id), f"{reg.team_name} ({player_count}/{team_player_amount})")
            )

        return [(series_name, team_list) for series_name, team_list in series_groups.items()]

def get_team_choices_with_context():
    with current_app.app_context():
        return get_flat_team_choices()

def get_team_players(team_id, session=None):
    """Get list of players for a specific team
    Args:
        team_id: The ID of the team
        session: Optional database session (uses db.session if not provided)
    Returns:
        List of tuples (player_id, player_name) for the team's roster
    """
    try:
        if not session:
            session = db.session
        
        with current_app.app_context():
            players = session.query(Player)\
                .join(RosterPlayersInSeries)\
                .filter(RosterPlayersInSeries.registration_id == team_id)\
                .all()
            return [(str(p.id), p.name) for p in players]
    except Exception as e:
        logging.error(f"Error getting team players: {e}")
        return []

def get_registration_choices():
    """Returns a list of tuples containing (id, label) for all registrations"""
    with current_app.app_context():
        try:
            registrations = db.session.query(SeriesRegistration)\
                .join(Series)\
                .order_by(Series.year.desc(), Series.name, SeriesRegistration.team_name)\
                .all()
            
            if not registrations:
                return [('', 'No registrations available')]
            
            choices = []
            for reg in registrations:
                try:
                    series_info = f"({reg.series.name} {reg.series.year})"
                    if reg.team_name:  # Team registration
                        label = f"{reg.team_name} {series_info}"
                    else:  # Personal registration
                        label = f"{reg.contact_player.name} {series_info}"
                    choices.append((str(reg.id), label))
                except Exception as e:
                    logging.error(f"Error processing registration {reg.id}: {e}")
                    continue
            
            return choices if choices else [('', 'No valid registrations found')]
        except Exception as e:
            logging.error(f"Database error in get_registration_choices: {e}")
            return [('', 'Error loading registrations')]

def get_series_participant_choices(series_id: int):
    """Get participant choices (teams or players) for a specific series.
    
    Args:
        series_id: ID of the series
        
    Returns:
        List of tuples (id, name) for form choices
    """
    with current_app.app_context():
        try:
            # Get series game type info
            series_query = db.session.query(Series)\
                .join(GameType)\
                .filter(Series.id == series_id)\
                .first()
            
            if not series_query:
                return []

            # For personal leagues (team_player_amount = 1)
            if series_query.game_type.team_player_amount == 1:
                participants = db.session.query(
                    SeriesRegistration.id,
                    Player.name
                ).join(
                    Player,
                    SeriesRegistration.contact_player_id == Player.id
                ).filter(
                    SeriesRegistration.series_id == series_id
                ).order_by(
                    Player.name
                ).all()
            else:
                # For team leagues
                participants = db.session.query(
                    SeriesRegistration.id,
                    SeriesRegistration.team_name
                ).filter(
                    SeriesRegistration.series_id == series_id,
                    SeriesRegistration.team_name.isnot(None)
                ).order_by(
                    SeriesRegistration.team_name
                ).all()

            return [(str(p.id), p.name if hasattr(p, 'name') else p.team_name) 
                    for p in participants]
            
        except Exception as e:
            logging.error(f"Error getting series participant choices: {e}")
            return []
