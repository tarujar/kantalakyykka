from flask_babel import lazy_gettext as _, gettext
from flask import flash
import re

def get_constraint_name(error_msg):
    # Check for both constraint "name" and constraint name_key patterns
    constraint_match = re.search(r'constraint ["\'](.+?)["\']|constraint (\w+)', str(error_msg))
    if constraint_match:
        return constraint_match.group(1) or constraint_match.group(2)
    return None

def handle_integrity_error(exc):
    error_msg = str(exc.orig)
    constraint_name = get_constraint_name(error_msg)
    
    # Map auto-generated constraint names to our custom ones
    constraint_mapping = {
        'teams_in_series_series_id_team_name_key': 'unique_team_name_in_series',
        'teams_in_series_series_id_team_abbreviation_key': 'unique_team_abbr_in_series'
    }
    
    if constraint_name:
        # Use mapped constraint name if it exists, otherwise use original
        translation_key = constraint_mapping.get(constraint_name, constraint_name)
        flash(_(translation_key), 'error')
    else:
        flash(_('database_constraint_was_violated'), 'error')
    return False

def handle_data_error(exc):
    flash(_('invalid_data_format'), 'error')
    return False

def validate_team_form(form):
    if form.team_abbreviation.data and len(form.team_abbreviation.data) > 10:
        flash(_('team_abbreviation_length_error'), 'error')
        return False
    if form.team_name.data and len(form.team_name.data) > 100:
        flash(_('team_name_length_error'), 'error')
        return False
    return True
