from flask_admin.contrib.sqla import ModelView
from flask_babel import lazy_gettext as _
from flask_admin.form import SecureForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from app.models.models import GameType
from app.utils import get_game_type_choices, get_series_choices
from app.utils import custom_gettext

class CustomModelView(ModelView):
    form_base_class = SecureForm
    field_flags = {"requiredif": True}  # Update to use dictionary
    name = "Custom Model"  # Add name attribute

    def _refresh_translations(self):
        if hasattr(self, 'column_labels'):
            self.column_labels = {key: custom_gettext(value) for key, value in self.column_labels.items()}
        if hasattr(self, 'form_labels'):
            self.form_labels = {key: custom_gettext(value) for key, value in self.form_labels.items()}
        if hasattr(self, 'form_extra_fields') and self.form_extra_fields:
            for field in self.form_extra_fields.values():
                if hasattr(field, 'label') and hasattr(field.label, 'text'):
                    field.label.text = custom_gettext(field.label.text)

    def __init__(self, model, session, **kwargs):
        # Ensure translations are updated when the view is initialized
        self._refresh_translations()
        super().__init__(model, session, **kwargs)

    def render(self, template, **kwargs):
        # Ensure translations are updated before rendering
        self._refresh_translations()
        return super().render(template, **kwargs)

class UserAdmin(CustomModelView):
    form_overrides = {
        'email': StringField,
        'hashed_password': PasswordField
    }
    column_labels = {
        'username': _('username'),
        'email': _('email'),
        'hashed_password': _('password'),
        'created_at': _('created_at')
    }
    form_labels = column_labels  # Use same translations for forms
    form_columns = ['username', 'email', 'hashed_password', 'created_at']

class PlayerAdmin(CustomModelView):
    form_overrides = {
        'email': StringField  # Ensure email field is correctly defined
    }
    column_labels = {
        'name': _('name'),
        'email': _('email'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'email', 'created_at']

class GameTypeAdmin(CustomModelView):
    form_overrides = {
        'max_players': IntegerField
    }
    column_labels = {
        'name': _('game_type'),
        'max_players': _('max_players'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'max_players', 'created_at']

class SeriesAdmin(CustomModelView):
    form_columns = ['name', 'season_type', 'year', 'status', 'registration_open', 'game_type_id']

    form_overrides = {
        'year': IntegerField
    }

    def __init__(self, model, session, **kwargs):
        choices, default = get_game_type_choices()
        self.form_extra_fields = {
            'game_type_id': SelectField(
                'game_type',
                choices=choices,
                default=default
            )
        }
        super().__init__(model, session, **kwargs)

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
        'created_at': _('created_at')
    }
    form_ajax_refs = {
        'game_type': {
            'fields': ['name'],
            'page_size': 10
        }
    }
    form_labels = column_labels

class TeamInSeriesAdmin(CustomModelView):
    def __init__(self, model, session, **kwargs):
        choices, default = get_series_choices()
        self.form_extra_fields = {
            'series_id': SelectField(
                'series',
                choices=choices,
                default=default
            )
        }
        super().__init__(model, session, **kwargs)

    column_labels = {
        'series_id': _('series'),
        'team_name': _('team_name'),
        'team_abbreviation': _('team_abbreviation'),
        'contact_player_id': _('contact_player'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['series_id', 'team_name', 'team_abbreviation', 'contact_player_id', 'created_at']

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

class GameAdmin(CustomModelView):
    def __init__(self, model, session, **kwargs):
        choices, default = get_series_choices()
        self.form_extra_fields = {
            'series_id': SelectField(
                'series',
                choices=choices,
                default=default
            )
        }
        super().__init__(model, session, **kwargs)

    column_labels = {
        'series_id': _('series'),
        'round': _('round'),
        'is_playoff': _('is_playoff'),
        'game_date': _('game_date'),
        'team_1_id': _('home_team'),
        'team_2_id': _('away_team'),
        'score_1_1': _('score_1_1'),
        'score_1_2': _('score_1_2'),
        'score_2_1': _('score_2_1'),
        'score_2_2': _('score_2_2'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['series_id', 'round', 'is_playoff', 'game_date', 'team_1_id', 'team_2_id', 'score_1_1', 'score_1_2', 'score_2_1', 'score_2_2', 'created_at']

class SingleThrowAdmin(CustomModelView):
    column_labels = {
        'throw_type': _('throw_type'),
        'throw_score': _('throw_score')
    }
    form_labels = column_labels
    form_columns = ['throw_type', 'throw_score']

class SingleRoundThrowAdmin(CustomModelView):
    column_labels = {
        'game_id': _('game'),
        'game_set_index': _('game_set_index'),
        'throw_position': _('throw_position'),
        'home_team': _('home_team'),
        'player_id': _('player'),
        'throw_1': _('throw_1'),
        'throw_2': _('throw_2'),
        'throw_3': _('throw_3'),
        'throw_4': _('throw_4')
    }
    form_labels = column_labels
    form_columns = ['game_id', 'game_set_index', 'throw_position', 'home_team', 'player_id', 'throw_1', 'throw_2', 'throw_3', 'throw_4']
