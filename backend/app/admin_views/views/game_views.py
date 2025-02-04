from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, StringField, DateField
from .base import CustomModelView
from app.utils.choices import get_series_choices, get_team_choices_by_series
from flask import redirect, url_for, request
from app.utils.display import format_team_name, format_series_name, format_end_game_score
import logging

class GameTypeAdmin(CustomModelView):
    form_overrides = {
        'max_players': IntegerField,
        'throw_round_amount': IntegerField 
    }
    column_labels = {
        'name': _('game_type'),
        'max_players': _('max_players'),
        'throw_round_amount': _('throw_round_amount'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'max_players', 'throw_round_amount', 'created_at'] 

class GameAdmin(CustomModelView):
    list_template = 'admin/game_form.html'
    
    # Add list row action permissions
    can_view_details = True
    can_edit = True
    can_delete = True

    def create_form(self, obj=None):
        form = super().create_form(obj)
        series_choices, _ = get_series_choices()
        team_choices = get_team_choices_by_series()
        
        # Set choices for series
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        
        # Set choices for teams
        team_list = []
        for series_name, teams in team_choices:
            team_list.extend([(str(id), f"{name} ({series_name})") for id, name in teams])
        
        form.team_1_id.choices = team_list
        form.team_2_id.choices = team_list
        
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        series_choices, _ = get_series_choices()
        team_choices = get_team_choices_by_series()
        
        # Set choices for series
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        
        # Set choices for teams
        team_list = []
        for series_name, teams in team_choices:
            team_list.extend([(str(id), f"{name} ({series_name})") for id, name in teams])
        
        form.team_1_id.choices = team_list
        form.team_2_id.choices = team_list
        
        return form

    def on_model_change(self, form, model, is_created):
        try:
            result = super().on_model_change(form, model, is_created)
            if is_created and 'next_step' in request.form:
                return redirect(url_for('gamescoresheetadmin.edit_view', id=model.id))
            return result
        except Exception as e:
            logging.error(f"Error in on_model_change: {e}")
            raise

    def __init__(self, model, session, **kwargs):
        self.form_extra_fields = {
            'series_id': SelectField('series', coerce=str),
            'team_1_id': SelectField('team_1', coerce=str),
            'team_2_id': SelectField('team_2', coerce=str)
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