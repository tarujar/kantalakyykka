from flask_babel import lazy_gettext as _
from wtforms import SelectField, IntegerField, BooleanField, FormField, FieldList
from flask_wtf import FlaskForm
from .base import CustomModelView
from app.utils.display import format_end_game_score
from app.utils.choices import get_series_choices, get_team_choices_by_series, get_player_choices_for_form, get_team_players
from flask_admin.form import BaseForm
from app.models.models import SingleThrow, SingleRoundThrow, Game
from flask import current_app, request, url_for, flash, redirect
from app.utils.throw_input import ThrowInputField
from app.services import GameService
from flask_admin import expose
import logging
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired, ValidationError
from app.utils.throw_input import ThrowType
from app.validators import validate_all_throws_not_zero
from app.utils.game_utils import process_single_throw, set_player_choices, load_existing_throws

class SingleRoundThrowForm(FlaskForm):
    class Meta:
        csrf = False  # Disable CSRF for nested form
    game_set_index = IntegerField(_('game_set_index'))
    throw_position = IntegerField(_('throw_position'))
    home_team = BooleanField(_('home_team'))
    player_id = SelectField(_('player'), coerce=str, choices=[], validators=[DataRequired()])  # Initialize with empty choices
    throw_1 = ThrowInputField(_('throw_1'))
    throw_2 = ThrowInputField(_('throw_2'))
    throw_3 = ThrowInputField(_('throw_3'))
    throw_4 = ThrowInputField(_('throw_4'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default player choices initialization
        # It will be set specifically for each team later

    def validate_player_id(self, field):
        """Custom validator for player_id"""
        if not field.data or field.data == '-1':
            raise ValidationError(_('Player selection is required'))
        # Check if the selected value is in choices
        if field.data not in [x[0] for x in field.choices]:
            self.logger.debug(f"Invalid player choice: {field.data}. Available choices: {field.choices}")
            raise ValidationError(_('Invalid player selection'))

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
    # Remove team_1_id and team_2_id fields since we don't need them
    team_1_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    team_2_round_throws = FieldList(FormField(TeamRoundThrowsForm), min_entries=1, max_entries=1)
    score_1_1 = IntegerField(_('score_1_1'))
    score_1_2 = IntegerField(_('score_1_2'))
    score_2_1 = IntegerField(_('score_2_1'))
    score_2_2 = IntegerField(_('score_2_2'))
    end_score_team_1 = IntegerField(_('end_score_team_1'))
    end_score_team_2 = IntegerField(_('end_score_team_2'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove team choices initialization
"""custom validation not used currently. don't remove or uncomment this code
    def validate(self):
        if not super().validate():
            return False

        # Use custom validation function
        try:
            validate_all_throws_not_zero(self, None)
        except ValidationError as e:
            self.throw_1.errors.append(str(e))
            return False

        return True"""

class GameScoreSheetAdmin(ModelView):  # Changed from CustomModelView to ModelView
    # Configuration
    endpoint = 'game_score_sheet'
    name = 'Game Score Sheet'
    category = 'statsit'
    
    # Templates
    edit_template = 'admin/game_score_sheet.html'
    create_template = 'admin/game_score_sheet.html'
    list_template = 'admin/model/list.html'

    # Permissions
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True

    # Form configuration
    form = GameScoreSheetForm  # Use our custom form

    def __init__(self, model, session, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.game_service = GameService()
        super().__init__(model, session, **kwargs)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_form_view(self):
        """Custom edit view"""
        self.logger.info("Edit form view called")
        id = request.args.get('id')
        self.logger.debug(f"Edit view for ID: {id}")
        
        if not id:
            self.logger.warning("No ID provided")
            return redirect(url_for('.index_view'))

        model = self.get_one(id)
        if not model:
            self.logger.warning(f"Record not found for ID: {id}")
            return redirect(url_for('.index_view'))

        if request.method == 'POST':
            form = GameScoreSheetForm(request.form)
            game = self.get_game(id)
            if game:
                # Set player choices before validation
                team1_players = get_team_players(game.team_1_id, self.session) or [(-1, 'No players')]
                team2_players = get_team_players(game.team_2_id, self.session) or [(-1, 'No players')]
                set_player_choices(form, team1_players, team2_players)
                
                self.logger.debug("Form data before validation:")
                self.logger.debug(f"Team 1 players: {team1_players}")
                self.logger.debug(f"Team 2 players: {team2_players}")
                self.logger.debug(f"Form data: {form.data}")

            self.logger.debug(f"Processing POST data for game {id}")
            if form.validate():
                self.logger.debug("Form validated successfully")
                try:
                    if request.form.get('form_type') == 'mobile':
                        self.process_mobile_form_submission(game.id, form)
                    else:
                        self.game_service.process_game_throws(model.id, form, self.session)
                    flash('Throws saved successfully!', 'success')
                    return redirect(url_for('.index_view'))
                except Exception as e:
                    self.logger.error(f"Error saving throws: {e}", exc_info=True)
                    flash('Error saving throws', 'error')
            else:
                self.logger.warning(f"Form validation failed: {form.errors}")
                flash('Form validation failed. Please correct the errors and try again.', 'error')

        # GET request or form validation failed
        form = GameScoreSheetForm()
        game = self.get_game(id)
        if game:
            team1_players = get_team_players(game.team_1_id, self.session) or [(-1, 'No players')]
            team2_players = get_team_players(game.team_2_id, self.session) or [(-1, 'No players')]
            
            set_player_choices(form, team1_players, team2_players)
            load_existing_throws(self.session, form, game)

        # Get the game type and throw round amount from the series
        game_type = game.series.game_type.name
        throw_round_amount = game.series.game_type.throw_round_amount

        return self.render(
            self.edit_template,
            form=form,
            model=model,
            game_type=game_type, 
            throw_round_amount=throw_round_amount,  
            return_url=url_for('.index_view')
        )

    def process_mobile_form_submission(self, game_id, form):
        """Process throws for the mobile form submission"""
        try:
            # Start fresh - rollback any existing transaction
            self.session.rollback()
            
            # Get existing throws
            existing_throws = self.session.query(SingleRoundThrow).filter_by(game_id=game_id).all()
            existing_throws_map = {(t.game_set_index, t.throw_position, t.home_team): t for t in existing_throws}
            
            # Process new throws in the specified order
            for round_num in range(1, 3):
                for player_index in range(2):
                    process_single_throw(self.session, self.game_service, game_id, form.team_1_round_throws.entries[0]['round_1'].entries[player_index], round_num, player_index + 1, True, existing_throws_map)
                    process_single_throw(self.session, self.game_service, game_id, form.team_2_round_throws.entries[0]['round_1'].entries[player_index], round_num, player_index + 1, False, existing_throws_map)
                for player_index in range(2, 4):
                    process_single_throw(self.session, self.game_service, game_id, form.team_1_round_throws.entries[0]['round_1'].entries[player_index], round_num, player_index + 1, True, existing_throws_map)
                    process_single_throw(self.session, self.game_service, game_id, form.team_2_round_throws.entries[0]['round_1'].entries[player_index], round_num, player_index + 1, False, existing_throws_map)
            
            # Commit all changes
            self.session.commit()
            self.logger.info("Successfully saved all throws for mobile form")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing throws for mobile form: {e}", exc_info=True)
            self.session.rollback()
            raise

    def get_game(self, game_id):
        return self.session.query(self.model).get(game_id)

    def get_throws(self, game_id):
        return self.session.query(SingleRoundThrow).filter_by(game_id=game_id).all()

    def create_form(self):
        self.logger.debug("Creating new form")
        form = super().create_form()
        return form

    def is_accessible(self):
        self.logger.debug("Checking view accessibility")
        return super().is_accessible()

    column_formatters = {
        'end_game_score': lambda v, c, m, p: format_end_game_score(m)

    }
    column_labels = {
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
    form_columns = ['round', 'is_playoff', 'game_date', 'team_1_id', 'team_2_id', 'score_1_1', 'score_1_2', 'score_2_1', 'score_2_2']
    column_list = form_columns + ['end_game_score', 'created_at']
