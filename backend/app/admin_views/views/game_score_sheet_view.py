from flask_babel import lazy_gettext as _
from flask_admin.contrib.sqla import ModelView
from flask import request, url_for, flash, redirect, jsonify
from flask_admin import expose
from app.utils.display import format_end_game_score
from app.utils.choices import get_team_players
from app.utils.game_utils import load_existing_throws, set_player_choices
from app.services.game_service import GameService
from app.forms.throw_forms import GameScoreSheetForm 
import logging
from app.utils.constants import GameScores  # Ensure this import is correct

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
        self.game_service = GameService()  # This will handle all throw processing
        super().__init__(model, session, **kwargs)

    def _flatten_form_errors(self, form_errors):
        """Flatten nested form errors into a dict of field_name: [error_messages]"""
        flattened = {}
        
        def _flatten(errors, prefix=''):
            for key, value in errors.items():
                if isinstance(value, (list, tuple)):
                    # Handle list of forms (like FieldList)
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            _flatten(item, f"{prefix}{key}-{i}-")
                        else:
                            field_name = f"{prefix}{key}"
                            flattened[field_name] = value
                            break
                elif isinstance(value, dict):
                    # Handle nested form
                    _flatten(value, f"{prefix}{key}-")
                else:
                    field_name = f"{prefix}{key}"
                    flattened[field_name] = value

        _flatten(form_errors)
        return flattened

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_form_view(self):
        game_id = request.args.get('id')
        if not game_id:
            flash('Game ID is required', 'error')
            return redirect(url_for('admin.index'))

        game = self.session.query(self.model).get(game_id)
        if not game:
            flash('Game not found', 'error')
            return redirect(url_for('admin.index'))

        game_type = game.series.game_type
        
        form = GameScoreSheetForm(request.form if request.method == 'POST' else None, game_type=game_type)
        
        team1_players = get_team_players(game.team_1_id, self.session) or [('-1', 'No players')]
        team2_players = get_team_players(game.team_2_id, self.session) or [('-1', 'No players')]

        if request.method == 'POST':
            if form.validate():
                try:
                    self.game_service.process_game_throws(game.id, form, self.session)
                    flash('Throws saved successfully!', 'success')
                    return redirect(url_for('.index_view'))
                except Exception as e:
                    self.logger.error(f"Error saving throws: {e}", exc_info=True)
                    flash('Error saving throws', 'error')
            else:
                return self.render(
                    self.edit_template,
                    form=form,
                    model=game,
                    game_constants=GameScores,
                    game_type=game_type,
                    throw_round_amount=game_type.throw_round_amount,
                    form_errors=self._flatten_form_errors(form.errors),
                    team1_players=team1_players,
                    team2_players=team2_players
                )

        # GET request
        load_existing_throws(self.session, form, game)

        # Add safer debug logging for form fields
        self.logger.debug("Form field values after loading:")
        if hasattr(form, '_fields'):
            for field_name, field in form._fields.items():
                try:
                    self.logger.debug(f"{field_name}: {field.data if hasattr(field, 'data') else 'NO DATA'}")
                except Exception as e:
                    self.logger.debug(f"Could not get data for {field_name}: {e}")

        return self.render(
            self.edit_template,
            form=form,
            model=game,
            game_constants=GameScores,
            game_type=game_type,
            throw_round_amount=game_type.throw_round_amount,
            team1_players=team1_players,
            team2_players=team2_players
        )

    def get_game(self, game_id):
        return self.session.query(self.model).get(game_id)

    def create_form(self):
        self.logger.debug("Creating new form")
        form = super().create_form()
        return form

    def is_accessible(self):
        self.logger.debug("Checking view accessibility")
        return super().is_accessible()

    def render(self, template, **kwargs):
        # Add GameScores to the template context
        kwargs['game_constants'] = GameScores
        return super().render(template, **kwargs)

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
    form_columns = ['round', 'is_playoff', 'game_date', 'team_1_id', 'team_2_id', 
                   'score_1_1', 'score_1_2', 'score_2_1', 'score_2_2']
    column_list = form_columns + ['end_game_score', 'created_at']

