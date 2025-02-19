from flask_admin.contrib.sqla import ModelView
from flask_babel import lazy_gettext as _
from flask_admin.form import SecureForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from app.models.models import GameType
from app.utils.choices import get_game_type_choices, get_series_choices, get_player_choices_with_contact
from app.utils.display import format_player_name, format_series_name, custom_gettext
from sqlalchemy.exc import IntegrityError, DataError
from flask import flash
import re

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

    def handle_view_exception(self, exc):
        if isinstance(exc, IntegrityError):
            if 'unique_team_name_in_series' in str(exc):
                flash('This team name already exists in the selected series', 'error')
            elif 'unique_team_abbr_in_series' in str(exc):
                flash('This team abbreviation already exists in the selected series', 'error')
            elif 'valid_email_format' in str(exc):
                flash('Please enter a valid email address', 'error')
            else:
                flash('A database constraint was violated. Please check your input.', 'error')
            return True

        if isinstance(exc, DataError):
            if 'value too long' in str(exc):
                match = re.search(r'value too long for type (\w+)\((\d+)\)', str(exc))
                if match:
                    field_type, length = match.groups()
                    flash(f'Input too long. Maximum length is {length} characters.', 'error')
                else:
                    flash('Input value is too long', 'error')
            else:
                flash('Invalid data format. Please check your input.', 'error')
            return True

        return super().handle_view_exception(exc)

    def _format_error_message(self, error):
        """Format error messages to be more user-friendly"""
        error_str = str(error)
        if 'NOT NULL' in error_str:
            return 'This field is required'
        if 'CHECK constraint' in error_str:
            if 'valid_throw_score' in error_str:
                return 'Score must be between -80 and 80 for valid throws, or 0 for invalid throws'
            if 'valid_throw_position' in error_str:
                return 'Throw position must be between 1 and 5'
            if 'valid_game_set_index' in error_str:
                return 'Game set index must be 1 or 2'
        return error_str

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
        'team_player_amount': IntegerField
    }
    column_labels = {
        'name': _('game_type'),
        'team_player_amount': _('team_player_amount'),
        'team_throws_in_set': _('team_throws_in_set'),
        'game_player_amount': _('game_player_amount'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'team_player_amount','team_throws_in_set','game_player_amount', 'created_at']

class SeriesAdmin(CustomModelView):
    form_columns = ['name', 'season_type', 'year', 'status', 'registration_open', 'game_type_id']

    form_overrides = {
        'year': IntegerField,
        'game_type_id': SelectField
    }

    def create_form(self):
        form = super().create_form()
        choices, default = get_game_type_choices()
        form.game_type_id.choices = choices
        form.game_type_id.coerce = int  # Add this line to ensure proper type conversion
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        choices, default = get_game_type_choices()
        form.game_type_id.choices = choices
        form.game_type_id.coerce = int  # Add this line to ensure proper type conversion
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
    column_list = ['series', 'team_name', 'team_abbreviation', 'contact_player_id', 'created_at']
    
    def create_form(self):
        form = super().create_form()
        series_choices, series_default = get_series_choices()
        player_choices, player_default = get_player_choices_with_contact()
        
        # Convert choices to integers for form processing
        form.series_id.choices = [(int(id), name) for id, name in series_choices]
        form.contact_player_id.choices = [(int(id), name) for id, name in player_choices]
        
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        series_choices, series_default = get_series_choices()
        player_choices, player_default = get_player_choices_with_contact()
        
        # Convert choices to integers for form processing
        form.series_id.choices = [(int(id), name) for id, name in series_choices]
        form.contact_player_id.choices = [(int(id), name) for id, name in player_choices]
        
        return form

    def __init__(self, model, session, **kwargs):
        self.form_extra_fields = {
            'series_id': SelectField(
                'series',
                coerce=int
            ),
            'contact_player_id': SelectField(
                'contact_player',
                coerce=int
            )
        }
        super().__init__(model, session, **kwargs)

    def validate_form(self, form):
        """Add custom validation messages"""
        if form.team_abbreviation.data and len(form.team_abbreviation.data) > 10:
            flash('Team abbreviation must be 10 characters or less', 'error')
            return False
        if form.team_name.data and len(form.team_name.data) > 100:
            flash('Team name must be 100 characters or less', 'error')
            return False
        return super().validate_form(form)

    column_labels = {
        'series_id': _('series'),
        'team_name': _('team_name'),
        'team_abbreviation': _('team_abbreviation'),
        'contact_player_id': _('contact_player'),
        'created_at': _('created_at')
    }

    # Add formatters to display names instead of IDs
    def _contact_player_formatter(view, context, model, name):
        return format_player_name(view.session, model.contact_player_id)

    def _series_formatter(view, context, model, name):
        if model.series:
            return f"{model.series.name} ({model.series.year})"
        return ''

    column_formatters = {
        'series': _series_formatter,
        'contact_player_id': _contact_player_formatter
    }

    form_labels = column_labels
    form_columns = ['series_id', 'team_name', 'team_abbreviation', 'contact_player_id', 'created_at']

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