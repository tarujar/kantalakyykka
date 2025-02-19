from flask_babel import lazy_gettext as _
from wtforms import SelectField
from flask_admin.model.form import InlineFormAdmin
from app.utils.choices import get_team_choices_with_player_count, get_player_choices_for_form, get_registration_choices
from .base import CustomModelView
from app.models import db, RosterPlayersInSeries, SeriesRegistration

class RosterAdmin(CustomModelView):
    column_list = ['registration_id', 'player_id']
    form_columns = ['registration_id', 'player_id']

    form_overrides = {
        'registration_id': SelectField,
        'player_id': SelectField,
    }

    def create_form(self):
        form = super().create_form()
        registration_choices = get_registration_choices()
        player_choices = [(str(id), name) for id, name in get_player_choices_for_form()]
        
        if not player_choices:
            player_choices = [('', 'No players available')]
            
        form.registration_id.choices = registration_choices
        form.player_id.choices = player_choices
        form.registration_id.coerce = str
        form.player_id.coerce = str
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        form.registration_id.choices = get_registration_choices()
        form.player_id.choices = [(str(id), name) for id, name in get_player_choices_for_form()] or [('', 'No players available')]
        form.registration_id.coerce = str
        form.player_id.coerce = str
        if obj is not None:
            form.registration_id.data = str(obj.registration_id)
            form.player_id.data = str(obj.player_id)
        return form

    def _registration_formatter(view, context, model, name):
        if not model or not model.registration:
            return "Unknown Registration"
        
        reg = model.registration
        series_info = f"({reg.series.name} {reg.series.year})" if reg.series else ""
        
        if reg.team_name:
            return f"{reg.team_name} {series_info}"
        elif reg.contact_player:
            return f"{reg.contact_player.name} {series_info}"
        return "Invalid Registration"

    def _player_formatter(view, context, model, name):
        if not model or not model.player:
            return "Unknown Player"
        return model.player.name

    column_formatters = {
        'registration_id': _registration_formatter,
        'player_id': _player_formatter
    }

    column_labels = {
        'registration_id': _('team'),
        'player_id': _('player')
    }

    form_labels = column_labels

    can_view_details = True
    can_export = True
    
    # Add these to help with error handling
    column_searchable_list = [
        'registration.team_name',
        'registration.contact_player.name',
        'player.name'
    ]
    column_filters = [
        'registration_id',
        'player_id',
        'registration.team_name',
        'registration.contact_player.name'
    ]

    # Add these to help with error handling
    create_template = 'admin/roster_select.html'
    edit_template = 'admin/roster_select.html'

    def render_create_form(self, form, **kwargs):
        """Override render_create_form to add team choices to the template context"""
        self._template_args['team_choices'] = get_team_choices_with_player_count()
        return super().render_create_form(form, **kwargs)

    def render_edit_form(self, form, **kwargs):
        """Override render_edit_form to add team choices to the template context"""
        self._template_args['team_choices'] = get_team_choices_with_player_count()
        return super().render_edit_form(form, **kwargs)

    def on_model_change(self, form, model, is_created):
        """Convert string IDs back to integers before saving to database"""
        model.registration_id = int(form.registration_id.data)
        model.player_id = int(form.player_id.data)
        return super().on_model_change(form, model, is_created)
