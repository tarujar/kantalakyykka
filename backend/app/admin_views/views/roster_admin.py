from flask_babel import lazy_gettext as _
from wtforms import SelectField
from flask_admin.model.form import InlineFormAdmin
from app.utils.choices import get_team_choices_with_player_count, get_player_choices_for_form
from .base import CustomModelView
from app.models import db, RosterPlayersInSeries

class RosterAdmin(CustomModelView):
    column_list = ['registration_id', 'player_id']
    form_columns = ['registration_id', 'player_id']

    form_overrides = {
        'registration_id': SelectField,
        'player_id': SelectField,
    }

    def create_form(self):
        form = super().create_form()
        # Keep the original grouped structure for the template
        self._template_args['team_choices'] = get_team_choices_with_player_count()
        
        # Flatten choices for form validation
        choices = []
        for _, team_list in get_team_choices_with_player_count():
            choices.extend([(str(id), name) for id, name in team_list])
        form.registration_id.choices = choices
        form.player_id.choices = [(str(id), name) for id, name in get_player_choices_for_form()]
        form.registration_id.coerce = str
        form.player_id.coerce = str
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        # Keep the original grouped structure for the template
        self._template_args['team_choices'] = get_team_choices_with_player_count()
        
        # Flatten choices for form validation
        choices = []
        for _, team_list in get_team_choices_with_player_count():
            choices.extend([(str(id), name) for id, name in team_list])
        form.registration_id.choices = choices
        form.player_id.choices = [(str(id), name) for id, name in get_player_choices_for_form()]
        form.registration_id.coerce = str
        form.player_id.coerce = str
        if obj is not None:
            form.registration_id.data = str(obj.registration_id)
            form.player_id.data = str(obj.player_id)
        return form

    def _team_formatter(view, context, model, name):
        if model.team:
            return f"{model.team.team_name} ({model.team.team_abbreviation}) - {model.team.series.name} {model.team.series.year}"
        return ''

    def _player_formatter(view, context, model, name):
        return model.player.name if model.player else ''

    column_formatters = {
        'registration_id': _team_formatter,
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
    column_searchable_list = ['player.name', 'team.team_name']
    column_filters = ['registration_id', 'player_id']

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

    column_searchable_list = ['player.name', 'team.team_name']
    column_filters = ['registration_id', 'player_id']
