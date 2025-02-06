from flask_babel import lazy_gettext as _
from flask_admin.contrib.sqla import ModelView
from flask import request, url_for, flash, redirect
from flask_admin import expose
from app.utils.display import format_end_game_score
from app.utils.choices import get_team_players
from app.utils.game_utils import load_existing_throws, set_player_choices
from app.services.game_service import GameService
from app.forms.throw_forms import GameScoreSheetForm 
import logging

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

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_form_view(self):
        id = request.args.get('id')
        if not id:
            return redirect(url_for('.index_view'))

        model = self.get_one(id)
        if not model:
            return redirect(url_for('.index_view'))

        if request.method == 'POST':
            form = GameScoreSheetForm(request.form)
            game = self.get_game(id)
            if game:
                team1_players = get_team_players(game.team_1_id, self.session) or [(-1, 'No players')]
                team2_players = get_team_players(game.team_2_id, self.session) or [(-1, 'No players')]
                set_player_choices(form, team1_players, team2_players)

            if form.validate():
                try:
                    self.game_service.process_game_throws(model.id, form, self.session)
                    flash('Throws saved successfully!', 'success')
                    return redirect(url_for('.index_view'))
                except Exception as e:
                    self.logger.error(f"Error saving throws: {e}", exc_info=True)
                    flash('Error saving throws', 'error')
            else:
                self.logger.warning(f"Form validation failed: {form.errors}")
                flash('Form validation failed', 'error')
                # Return the same form with errors
                return self.render(
                    self.edit_template,
                    form=form,
                    model=model,
                    return_url=url_for('.index_view')
                )

        # GET request
        form = GameScoreSheetForm()
        game = self.get_game(id)
        if game:
            team1_players = get_team_players(game.team_1_id, self.session) or [(-1, 'No players')]
            team2_players = get_team_players(game.team_2_id, self.session) or [(-1, 'No players')]
            
            set_player_choices(form, team1_players, team2_players)
            load_existing_throws(self.session, form, game)

        return self.render(
            self.edit_template,
            form=form,
            model=model,
            return_url=url_for('.index_view')
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

