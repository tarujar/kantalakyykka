from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, StringField, DateField
from wtforms.validators import DataRequired
from flask_admin.base import expose
from .base import CustomModelView
from app.utils.choices import get_series_choices, get_team_choices_by_series, get_series_participant_choices
from flask import redirect, url_for, request, render_template
from app.utils.display import format_team_name, format_series_name, format_end_game_score
import logging

class GameTypeAdmin(CustomModelView):
    form_overrides = {
        'team_player_amount': IntegerField,
        'game_player_amount': IntegerField,
        'team_throws_in_set': IntegerField,
        'throw_round_amount': IntegerField,
        'kyykka_amount': IntegerField,

    }
    column_labels = {
        'name': _('game_type'),
        'team_player_amount': _('team_player_amount'),
        'game_player_amount': _('game_player_amount'),
        'team_throws_in_set': _('team_throws_in_set'),
        'throw_round_amount': _('throw_round_amount'),
        'kyykka_amount': _('kyykka_amount'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['name', 'team_player_amount','game_player_amount','team_throws_in_set', 'throw_round_amount','kyykka_amount'] 

class GameAdmin(CustomModelView):
    list_template = 'admin/game_list.html'
    create_template = 'admin/model/create.html'
    # Add list row action permissions
    can_view_details = True
    can_edit = True
    can_delete = True

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        # For GET requests, check if we need to show series selection
        if request.method == 'GET' and not request.args.get('series_id'):
            series_choices, _ = get_series_choices()
            # Pass the admin_view to the template context
            return self.render('admin/game_series_select.html', 
                series_choices=series_choices,
                admin_view=self)
        return super().create_view()

    def create_form(self, obj=None):
        form = super().create_form(obj)
        series_choices, _ = get_series_choices()
        form.series_id.choices = [('', '-- Select Series --')] + [
            (str(id), f"{name} ({year})") for id, name, year in series_choices
        ]
        
        # Handle series_id from URL
        series_id = request.args.get('series_id')
        if series_id:
            form.series_id.data = series_id
            team_choices = get_series_participant_choices(int(series_id))
            form.team_1_id.choices = [('', '-- Select Team --')] + team_choices
            form.team_2_id.choices = [('', '-- Select Team --')] + team_choices
        else:
            form.team_1_id.choices = [('', '-- Select Team --')]
            form.team_2_id.choices = [('', '-- Select Team --')]
        
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        
        # Make series_id field read-only in edit mode
        form.series_id.render_kw = {'readonly': True, 'disabled': 'disabled'}
        series_choices, _ = get_series_choices()

        # Set choices for series with a default empty option
        form.series_id.choices = [('', '-- Select Series --')] + [
            (str(id), f"{name} ({year})") for id, name, year in series_choices
        ]
        
        # Set empty choices with default option
        empty_choice = [('', '-- Select Team --')]
        
        # Get team choices based on the game's series
        if obj and obj.series_id:
            team_choices = get_series_participant_choices(obj.series_id)
            if team_choices:
                form.team_1_id.choices = empty_choice + team_choices
                form.team_2_id.choices = empty_choice + team_choices
            else:
                form.team_1_id.choices = empty_choice
                form.team_2_id.choices = empty_choice
        else:
            form.team_1_id.choices = empty_choice
            form.team_2_id.choices = empty_choice
        
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
            'series_id': SelectField('series', coerce=str, render_kw={'readonly': True,'disabled': 'disabled'}),
            'team_1_id': SelectField('team_1', coerce=str, validators=[DataRequired(message='Please select team 1')]),
            'team_2_id': SelectField('team_2', coerce=str, validators=[DataRequired(message='Please select team 2')])
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