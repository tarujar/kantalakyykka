from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList
from .base import CustomModelView
from app.utils.choices import get_series_choices, get_team_choices_by_series
from flask import current_app
from app.utils.display import format_team_name, format_series_name, format_end_game_score
from flask_admin.form import BaseForm
from flask_admin.model.form import InlineFormAdmin
from app.models.models import SingleRoundThrow

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


class GameAdmin(CustomModelView):
    def set_team_choices(self, form):
        series_choices, series_default = get_series_choices()
        team_choices = get_team_choices_by_series()
        
        # Convert choices to strings for form processing
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        
        def set_choices(field, choices):
            field.choices = []
            for series_name, teams in choices:
                field.choices.extend([(str(id), f"{name} ({series_name})") for id, name in teams])
        
        set_choices(form.team_1_id, team_choices)
        set_choices(form.team_2_id, team_choices)

    def create_form(self):
        form = super().create_form()
        self.set_team_choices(form)
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        self.set_team_choices(form)
        return form

    def __init__(self, model, session, **kwargs):
        self.form_extra_fields = {
            'series_id': SelectField(
                'series',
                coerce=str
            ),
            'team_1_id': SelectField(
                'team_1',
                coerce=str
            ),
            'team_2_id': SelectField(
                'team_2',
                coerce=str
            )
        }
        super().__init__(model, session, **kwargs)

    def _team_formatter(view, context, model, name):
        return format_team_name(view.session, getattr(model, name))
    def _series_formatter(view, context, model, name):
        return format_series_name(view.session, getattr(model, name))

    column_formatters = {
        'team_1_id': _team_formatter,
        'team_2_id': _team_formatter,
        'series_id': _series_formatter,
        'end_game_score': lambda v, c, m, p: format_end_game_score(m)
    }

    column_labels = {
        'series_id': _('series'),
        'round': _('round'),
        'is_playoff': _('is_playoff'),
        'game_date': _('game_date'),
        'team_1_id': _('team_1'),
        'team_2_id': _('team_2'),
        'score_1_1': _('score_1_1'),
        'score_1_2': _('score_1_2'),
        'score_2_1': _('score_2_1'),
        'score_2_2': _('score_2_2'),
        'created_at': _('created_at'),
        'end_game_score': _('end_game_score')
    }
    form_labels = column_labels
    form_columns = ['series_id', 'round', 'is_playoff', 'game_date', 'team_1_id', 'team_2_id', 'score_1_1', 'score_1_2', 'score_2_1', 'score_2_2']
    column_list = form_columns + ['end_game_score','created_at']


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
    column_list = ['game_id', 'game_set_index', 'throw_position', 'home_team', 'player_id', 'throw_1', 'throw_2', 'throw_3', 'throw_4']