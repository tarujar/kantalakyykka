from flask_admin.contrib.sqla import ModelView
from flask import request, url_for, flash, redirect
from flask_admin import expose
from forms.throw_forms import GameScoreSheetForm
from services.throw_service import ThrowService
from models.models import ThrowType, SingleThrow, SingleRoundThrow

import logging

class GameScoreSheetAdmin(ModelView):
    def __init__(self, model, session, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.throw_service = ThrowService()
        super().__init__(model, session, **kwargs)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_form_view(self):
        """Handle game score sheet editing"""
        id = request.args.get('id')
        if not id:
            return redirect(url_for('.index_view'))

        model = self.get_one(id)
        if not model:
            return redirect(url_for('.index_view'))

        if request.method == 'POST':
            return self._handle_post_request(model, id)

        return self._handle_get_request(model)

    def _handle_post_request(self, model, id):
        """Handle POST request for game score sheet"""
        form = GameScoreSheetForm(request.form)
        self._setup_form(form, id)

        if form.validate():
            try:
                self._save_throws(model.id, form)
                flash('Throws saved successfully!', 'success')
                return redirect(url_for('.index_view'))
            except Exception as e:
                self.logger.error(f"Error saving throws: {e}", exc_info=True)
                flash('Error saving throws', 'error')
        else:
            self.logger.warning(f"Form validation failed: {form.errors}")
            flash('Form validation failed', 'error')

        return self.render(
            self.edit_template,
            form=form,
            model=model,
            return_url=url_for('.index_view')
        )

    def _handle_get_request(self, model):
        """Handle GET request for game score sheet"""
        form = GameScoreSheetForm()
        self._setup_form(form, model.id)
        return self.render(
            self.edit_template,
            form=form,
            model=model,
            return_url=url_for('.index_view')
        )

    def _setup_form(self, form, game_id):
        """Setup form with player choices and existing throws"""
        game = self.get_game(game_id)
        if game:
            self._set_player_choices(form, game)
            self._load_existing_throws(form, game)

    def _set_player_choices(self, form, game):
        """Set player choices for form fields"""
        team1_players = self._get_team_players(game.team_1_id) or [(-1, 'No players')]
        team2_players = self._get_team_players(game.team_2_id) or [(-1, 'No players')]
        
        for team_index, (throws, players) in enumerate([(form.team_1_round_throws, team1_players), 
                                                      (form.team_2_round_throws, team2_players)]):
            for entry in throws:
                for round_num in [1, 2]:
                    for throw_form in entry[f'round_{round_num}'].entries:
                        throw_form.player_id.choices = players
                        throw_form.home_team.data = (team_index == 0)

    def _get_team_players(self, team_id):
        """Get list of players for a team"""
        from app.utils.choices import get_team_players
        return get_team_players(team_id, self.session)

    def _load_existing_throws(self, form, game):
        """Load existing throws into form"""
        throws = self._get_throws(game.id)
        if not throws:
            return

        self._load_scores(form, game)
        self._load_throw_data(form, throws)

    def _load_scores(self, form, game):
        """Load scores into form"""
        form.score_1_1.data = game.score_1_1
        form.score_1_2.data = game.score_1_2
        form.score_2_1.data = game.score_2_1
        form.score_2_2.data = game.score_2_2
        form.end_score_team_1.data = game.score_1_1 + game.score_1_2
        form.end_score_team_2.data = game.score_2_1 + game.score_2_2

    def _load_throw_data(self, form, throws):
        """Load throw data into form"""
        for throw in throws:
            try:
                throw_form = self._get_throw_form(form, throw)
                if throw_form:
                    self._set_throw_form_data(throw_form, throw)
            except (IndexError, AttributeError) as e:
                self.logger.error(f"Error loading throw data: {e}")

    def _get_throw_form(self, form, throw):
        """Get the appropriate throw form based on team and position"""
        team_field = form.team_1_round_throws if throw.home_team else form.team_2_round_throws
        try:
            return team_field.entries[0][f'round_{throw.game_set_index}'].entries[throw.throw_position - 1]
        except (IndexError, KeyError):
            return None

    def _set_throw_form_data(self, throw_form, throw):
        """Set data for a single throw form"""
        throw_form.player_id.data = str(throw.player_id)
        throw_form.game_set_index.data = throw.game_set_index
        throw_form.throw_position.data = throw.throw_position
        throw_form.home_team.data = throw.home_team

        for i, throw_id in enumerate([throw.throw_1, throw.throw_2, throw.throw_3, throw.throw_4], 1):
            if throw_id:
                single_throw = self.session.query(SingleThrow).get(throw_id)
                if single_throw:
                    setattr(throw_form, f'throw_{i}', self._get_throw_value(single_throw))

    def _get_throw_value(self, throw):
        """Convert throw object to display value"""
        from app.utils.throw_input import ThrowInputField
        return ThrowInputField.get_throw_value(throw)

    def _save_throws(self, game_id, form):
        """Save throws for a game"""
        for team_index, team_throws in enumerate([form.team_1_round_throws, form.team_2_round_throws]):
            is_home_team = team_index == 0
            for entry in team_throws:
                for round_num in [1, 2]:
                    self._save_round_throws(game_id, entry, round_num, is_home_team)

    def _save_round_throws(self, game_id, entry, round_num, is_home_team):
        """Save throws for a single round"""
        round_data = getattr(entry, f'round_{round_num}')
        for pos, throw_form in enumerate(round_data, 1):
            self.throw_service.save_round_throw(
                self.session,
                game_id=game_id,
                round_num=round_num,
                position=pos,
                is_home_team=is_home_team,
                player_id=throw_form.player_id.data,
                throws=[
                    throw_form.throw_1.data,
                    throw_form.throw_2.data,
                    throw_form.throw_3.data,
                    throw_form.throw_4.data
                ]
            )

    def get_game(self, game_id):
        """Get game by ID"""
        return self.session.query(self.model).get(game_id)

    def _get_throws(self, game_id):
        """Get throws for a game"""
        return self.session.query(SingleRoundThrow).filter_by(game_id=game_id).all()
