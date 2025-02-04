from flask_babel import lazy_gettext as _
from wtforms import IntegerField, SelectField, StringField, BooleanField
from flask_admin.contrib.sqla import ModelView
from app.utils.choices import get_game_type_choices
from app.models.models import Series

class SeriesAdmin(ModelView):
    form_columns = ['name', 'season_type', 'year', 'status', 'registration_open', 'game_type_id', 'is_cup_league']

    form_overrides = {
        'year': IntegerField,
        'game_type_id': SelectField
    }

    def create_form(self):
        form = super().create_form()
        choices, default = get_game_type_choices()
        form.game_type_id.choices = choices
        form.game_type_id.coerce = int  # Ensure proper type conversion
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        choices, default = get_game_type_choices()
        form.game_type_id.choices = choices
        form.game_type_id.coerce = int  # Ensure proper type conversion
        return form

    def _game_type_formatter(view, context, model, name):
        return model.game_type.name if model.game_type else ''

    column_formatters = {
        'game_type': _game_type_formatter
    }

    column_labels = {
        'name': _('series'),
        'season_type': _('season_type'),
        'year': _('year'),
        'status': _('status'),
        'registration_open': _('registration_open'),
        'game_type_id': _('game_type'),
        'created_at': _('created_at'),
        'is_cup_league': _('is_cup_league')
    }
    form_ajax_refs = {
        'game_type': {
            'fields': ['name'],
            'page_size': 10
        }
    }
    form_labels = column_labels
    column_list = ['name', 'season_type', 'game_type', 'year', 'status', 'registration_open','is_cup_league']


