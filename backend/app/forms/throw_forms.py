from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList, Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app.utils.throw_input import ThrowInputField
from app.utils.game_constants import GameScores
import logging

class SingleRoundThrowForm(FlaskForm):
    """Form for single_round_throws table"""
    class Meta:
        csrf = False
    game_set_index = IntegerField(_('game_set_index'), validators=[DataRequired()])
    throw_position = IntegerField(_('throw_position'), validators=[DataRequired()])
    home_team = BooleanField(_('home_team'))
    team_id = IntegerField(_('team_id'))
    player_id = SelectField(_('player'), coerce=str, choices=[])
    # Use ThrowInputField directly for the throws
    throw_1 = ThrowInputField(_('throw_1'), validators=[DataRequired()])
    throw_2 = ThrowInputField(_('throw_2'), validators=[DataRequired()])
    throw_3 = ThrowInputField(_('throw_3'), validators=[DataRequired()])
    throw_4 = ThrowInputField(_('throw_4'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.player_id.choices:
            self.player_id.choices = [('-1', '-- Select Player --')]

    def validate_player_id(self, field):
        if not field.data or field.data == '-1':
            raise ValidationError(_('Player selection is required'))
        if field.data not in [x[0] for x in field.choices]:
            raise ValidationError(_('Invalid player selection'))

class TeamRoundThrowsForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        self.game_type = kwargs.pop('game_type', None)
        super().__init__(*args, **kwargs)

        if self.game_type:
            # Pre-define all round fields before any initialization
            self.logger = logging.getLogger(__name__)
            self.logger.debug(f"Initializing TeamRoundThrowsForm with game_type: {self.game_type}")
            
            for round_num in range(1, self.game_type.throw_round_amount + 1):
                field_name = f'round_{round_num}'
                self.logger.debug(f"Creating field {field_name}")
                
                # Create the field list
                field = FieldList(FormField(SingleRoundThrowForm), min_entries=1)
                
                # Bind the field to the form
                field = field.bind(form=self, name=field_name)
                setattr(self, field_name, field)
                
                # Initialize with one entry
                self.logger.debug(f"Initializing entry for {field_name}")
                field.append_entry()
                entry = field.entries[0]
                entry.game_set_index.data = round_num
                entry.throw_position.data = 1

class GameScoreSheetForm(Form):
    team_1_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    team_2_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    # Always have 4 score fields as per game table structure
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
        self.game_type = kwargs.pop('game_type', None)
        super().__init__(formdata, **kwargs)
        
        logger = logging.getLogger(__name__)
        logger.debug(f"Initializing GameScoreSheetForm with game_type: {self.game_type}")

        if self.game_type:
            # Initialize team round forms with game type
            for field_name in ['team_1_round_throws', 'team_2_round_throws']:
                field = getattr(self, field_name)
                logger.debug(f"Setting up {field_name}")
                
                if not field.entries:
                    # Create new TeamRoundThrowsForm with game_type
                    form_data = {'csrf': False}
                    if formdata:
                        prefix = f"{field_name}-0-"
                        form_data.update({
                            k[len(prefix):]: v 
                            for k, v in formdata.items() 
                            if k.startswith(prefix)
                        })
                    
                    # Create entry with game_type
                    field.append_entry(form_data)
                    entry = field.entries[0]
                    entry.game_type = self.game_type
                    logger.debug(f"Created entry for {field_name} with game_type")

    def __contains__(self, key):
        """Allow checking if score fields exist"""
        if key.startswith('score_'):
            return key in self._fields
        return super().__contains__(key)