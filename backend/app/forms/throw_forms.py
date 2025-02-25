from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList, Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app.utils.throw_input import ThrowInputField
from app.utils.constants import GameScores
import logging

class SingleRoundThrowForm(FlaskForm):
    """Form for single_round_throws table"""
    class Meta:
        csrf = False
    game_set_index = IntegerField(_('game_set_index'), validators=[DataRequired()])
    throw_position = IntegerField(_('throw_position'), validators=[DataRequired()])
    home_team = BooleanField(_('home_team'))
    team_id = IntegerField(_('team_id'))
    
    # Add separate player fields for both players
    player_1_id = SelectField(_('player_1'), coerce=str, choices=[])
    player_2_id = SelectField(_('player_2'), coerce=str, choices=[])
    
    # Player 1 throws
    throw_1 = ThrowInputField(_('throw_1'), validators=[DataRequired()])
    throw_2 = ThrowInputField(_('throw_2'), validators=[DataRequired()])
    
    # Player 2 throws
    throw_3 = ThrowInputField(_('throw_3'), validators=[DataRequired()])
    throw_4 = ThrowInputField(_('throw_4'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.player_1_id.choices:
            self.player_1_id.choices = [('-1', '-- Select Player 1 --')]
        if not self.player_2_id.choices:
            self.player_2_id.choices = [('-1', '-- Select Player 2 --')]

    def validate_player_1_id(self, field):
        if not field.data or field.data == '-1':
            raise ValidationError(_('Player 1 selection is required'))
        if field.data not in [x[0] for x in field.choices]:
            raise ValidationError(_('Invalid player selection'))

    def validate_player_2_id(self, field):
        if not field.data or field.data == '-1':
            raise ValidationError(_('Player 2 selection is required'))
        if field.data not in [x[0] for x in field.choices]:
            raise ValidationError(_('Invalid player selection'))

class TeamRoundThrowsForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.game_type = kwargs.pop('game_type', None)
        
        # Initialize base form first
        super().__init__(*args, **kwargs)

        if self.game_type:
            self.logger.debug(f"Initializing TeamRoundThrowsForm with game_type: {self.game_type}")
            
            # Create round fields based on game type
            for round_num in range(1, self.game_type.throw_round_amount + 1):
                field_name = f'round_{round_num}'
                
                # Create the field
                round_form = SingleRoundThrowForm()
                field = FormField(SingleRoundThrowForm, default=round_form)
                
                # Add field to form
                setattr(self, field_name, field)
                field.bind(form=self, name=field_name)
                self._fields[field_name] = field
                
                # Initialize field data
                if field.form:
                    field.form.game_set_index.data = 1
                    field.form.throw_position.data = round_num
                
                self.logger.debug(f"Created and bound field {field_name}")

    def get_round(self, round_num):
        """Safe method to get round data"""
        field_name = f'round_{round_num}'
        if field_name in self._fields:
            return self._fields[field_name]
        self.logger.error(f"Field {field_name} not found in {list(self._fields.keys())}")
        return None

    def __iter__(self):
        """Yield all form fields including dynamically added ones"""
        for name, field in self._fields.items():
            yield field

    def __getattr__(self, name):
        """Handle dynamic round field access"""
        if name.startswith('round_'):
            if name in self._fields:
                return self._fields[name]
            self.logger.error(f"Field {name} not found in {list(self._fields.keys())}")
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

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

        if not self.game_type:
            logger.error("No game type provided!")
            return

        # Initialize team round forms with game type
        for field_name in ['team_1_round_throws', 'team_2_round_throws']:
            field = getattr(self, field_name)
            logger.debug(f"Setting up {field_name}")
            
            if not field.entries:
                # Pass game_type when creating new entries
                field.append_entry({'game_type': self.game_type})
                entry = field.entries[0]
                entry.game_type = self.game_type
                logger.debug(f"Created entry for {field_name} with game_type")

    def __contains__(self, key):
        """Allow checking if score fields exist"""
        if key.startswith('score_'):
            return key in self._fields
        return super().__contains__(key)