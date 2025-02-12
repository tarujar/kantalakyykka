from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app.utils.throw_input import ThrowInputField
from app.utils.game_constants import GameScores

class SingleRoundThrowForm(FlaskForm):
    class Meta:
        csrf = False
    game_set_index = IntegerField(_('game_set_index'), validators=[DataRequired()])
    throw_position = IntegerField(_('throw_position'), validators=[DataRequired()])
    home_team = BooleanField(_('home_team'))
    player_id = SelectField(_('player'), coerce=str, choices=[], validators=[DataRequired()])
    throw_1 = ThrowInputField(_('throw_1'), validators=[DataRequired()])
    throw_2 = ThrowInputField(_('throw_2'), validators=[DataRequired()])
    throw_3 = ThrowInputField(_('throw_3'), validators=[DataRequired()])
    throw_4 = ThrowInputField(_('throw_4'), validators=[DataRequired()])

    def validate_player_id(self, field):
        if not field.data or field.data == '-1':
            raise ValidationError(_('Player selection is required'))
        if field.data not in [x[0] for x in field.choices]:
            raise ValidationError(_('Invalid player selection'))

class TeamRoundThrowsForm(FlaskForm):
    class Meta:
        csrf = False
    round_1 = FieldList(FormField(SingleRoundThrowForm), min_entries=4, max_entries=4)
    round_2 = FieldList(FormField(SingleRoundThrowForm), min_entries=4, max_entries=4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set both game_set_index and throw_position for each round
        for round_num, round_field in [(1, self.round_1), (2, self.round_2)]:
            for i, form in enumerate(round_field.entries, 1):
                form.game_set_index.data = round_num
                form.throw_position.data = i
                #print(f"Set round {round_num}, position {i}")

class GameScoreSheetForm(FlaskForm):
    team_1_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    team_2_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    score_1_1 = IntegerField(_('score_1_1'), 
        validators=[DataRequired(), NumberRange(
            min=GameScores.ROUND_SCORE_MIN, 
            max=GameScores.ROUND_SCORE_MAX,
            message=_('Round score must be between %(min)d and %(max)d')
        )])
    score_1_2 = IntegerField(_('score_1_2'), 
        validators=[DataRequired(), NumberRange(
            min=GameScores.ROUND_SCORE_MIN, 
            max=GameScores.ROUND_SCORE_MAX
        )])
    score_2_1 = IntegerField(_('score_2_1'), 
        validators=[DataRequired(), NumberRange(
            min=GameScores.ROUND_SCORE_MIN, 
            max=GameScores.ROUND_SCORE_MAX
        )])
    score_2_2 = IntegerField(_('score_2_2'), 
        validators=[DataRequired(), NumberRange(
            min=GameScores.ROUND_SCORE_MIN, 
            max=GameScores.ROUND_SCORE_MAX
        )])
    end_score_team_1 = IntegerField(_('end_score_team_1'))
    end_score_team_2 = IntegerField(_('end_score_team_2'))

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)
        # Initialize throw positions for both teams
        for team_throws in [self.team_1_round_throws, self.team_2_round_throws]:
            for team_round in team_throws:
                for round_num in [1, 2]:
                    round_field = getattr(team_round, f'round_{round_num}')
                    for i, form in enumerate(round_field, 1):
                        form.throw_position.data = i