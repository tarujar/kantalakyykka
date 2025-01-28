from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList
from flask_wtf import FlaskForm
from .base import CustomModelView
from app.utils.choices import get_series_choices, get_team_choices_by_series, get_player_choices_for_form
from flask_admin.form import BaseForm
from app.models.models import SingleThrow, SingleRoundThrow
from flask import current_app
from app.utils.throw_input import ThrowInputField

class SingleRoundThrowForm(FlaskForm):
    class Meta:
        csrf = False  # Disable CSRF for nested form
    game_set_index = IntegerField(_('game_set_index'))
    throw_position = IntegerField(_('throw_position'))
    home_team = BooleanField(_('home_team'))
    player_id = SelectField(_('player'), coerce=int)
    throw_1 = ThrowInputField(_('throw_1'))
    throw_2 = ThrowInputField(_('throw_2'))
    throw_3 = ThrowInputField(_('throw_3'))
    throw_4 = ThrowInputField(_('throw_4'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with current_app.app_context():
            self.player_id.choices = get_player_choices_for_form()

class TeamRoundThrowsForm(FlaskForm):
    class Meta:
        csrf = False  # Disable CSRF for nested form
    round_1 = FieldList(FormField(SingleRoundThrowForm), min_entries=4, max_entries=4)
    round_2 = FieldList(FormField(SingleRoundThrowForm), min_entries=4, max_entries=4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, form in enumerate(self.round_1.entries):
            form.game_set_index.data = 1
        for i, form in enumerate(self.round_2.entries):
            form.game_set_index.data = 2

class GameScoreSheetForm(FlaskForm):
    series_id = SelectField(_('series'), coerce=int)
    team_1_id = SelectField(_('team_1'), coerce=int)
    team_2_id = SelectField(_('team_2'), coerce=int)
    team_1_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    team_2_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.series_id.choices = get_series_choices()[0]
        self.team_1_id.choices = get_team_choices_by_series()
        self.team_2_id.choices = get_team_choices_by_series()

class GameScoreSheetAdmin(CustomModelView):
    form = GameScoreSheetForm
    edit_template = 'admin/game_score_sheet.html'
    create_template = 'admin/game_score_sheet.html'

    def create_form(self):
        form = super().create_form()
        self.set_team_choices(form)
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        self.set_team_choices(form)
        return form

    def set_team_choices(self, form):
        series_choices, series_default = get_series_choices()
        team_choices = get_team_choices_by_series()
        
        form.series_id.choices = [(str(id), f"{name} ({year})") for id, name, year in series_choices]
        
        def set_choices(field, choices):
            field.choices = []
            for series_name, teams in choices:
                field.choices.extend([(str(id), f"{name} ({series_name})") for id, name in teams])
        
        set_choices(form.team_1_id, team_choices)
        set_choices(form.team_2_id, team_choices)

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
    form_columns = ['series_id', 'round', 'is_playoff', 'game_date', 'team_1_id', 'team_2_id', 'score_1_1', 'score_1_2', 'score_2_1', 'score_2_2', 'team_1_round_throws', 'team_2_round_throws']
    column_list = form_columns + ['end_game_score', 'created_at']
