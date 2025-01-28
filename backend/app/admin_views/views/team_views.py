from flask_babel import lazy_gettext as _
from wtforms import StringField, SelectField
from .base import CustomModelView
from app.utils.choices import get_series_choices, get_player_choices
from app.utils.display import format_series_name, format_player_contact_info
from flask import flash
from app.utils.validation_messages import validate_team_form

class TeamHistoryAdmin(CustomModelView):
    column_labels = {
        'previous_registration_id': _('previous_registration'),
        'next_registration_id': _('next_registration'),
        'relation_type': _('relation_type'),
        'notes': _('notes'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['previous_registration_id', 'next_registration_id', 'relation_type', 'notes', 'created_at']


class PlayerAdmin(CustomModelView):
    form_overrides = {
        'email': StringField
    }
    column_labels = {
        'name': _('name'),
        'email': _('email'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'email', 'created_at']



class TeamInSeriesAdmin(CustomModelView):
    form_columns = ['series_id', 'team_name', 'team_abbreviation', 'contact_player_id', 'group']
    column_list = form_columns + ['created_at']
    
    def create_form(self):
        form = super().create_form()
        series_choices, series_default = get_series_choices()
        player_choices = get_player_choices()
        
        # Convert choices to strings for form processing
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        form.contact_player_id.choices = [(str(id), f"{name} ({email})") for id, name, email in player_choices]
        
        # Explicitly remove any redundant Player field if it exists
        if 'player_id' in form._fields:
            del form._fields['player_id']
        
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        series_choices, series_default = get_series_choices()
        player_choices = get_player_choices()
        
        # Convert choices to strings for form processing
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        form.contact_player_id.choices = [(str(id), f"{name} ({email})") for id, name, email in player_choices]
    
        return form

    def __init__(self, model, session, **kwargs):
        self.form_extra_fields = {
            'series_id': SelectField(
                'series',
                coerce=str
            ),
            'contact_player_id': SelectField(
                'contact_player',
                coerce=str
            )
        }
        super().__init__(model, session, **kwargs)
 
    def validate_form(self, form):
        if not validate_team_form(form):
            return False
        return super().validate_form(form)

    column_labels = {
        'series_id': _('series'),
        'team_name': _('team_name'),
        'team_abbreviation': _('team_abbreviation'),
        'contact_player_id': _('contact_player'),
        'created_at': _('created_at'),
        'group': _('group')
    }

    # Add formatters to display names instead of IDs
    def _contact_player_formatter(view, context, model, name):
        return format_player_contact_info(view.session, model.contact_player_id)

    def _series_formatter(view, context, model, name):
        return format_series_name(view.session, model.series_id)

    column_formatters = {
        'series': _series_formatter,
        'contact_player_id': _contact_player_formatter,
        'series_id': _series_formatter  # Ensure this line formats series_id
    }

    form_labels = column_labels
