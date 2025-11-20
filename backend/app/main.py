from flask import Flask, request
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext as _
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config.update(
    BABEL_DEFAULT_LOCALE='fi',
    BABEL_TRANSLATION_DIRECTORIES=os.path.abspath(os.path.join(os.path.dirname(__file__), '../translations')),
    LANGUAGES=['fi', 'en']
)
app.jinja_env.globals.update(hasattr=hasattr)

db = SQLAlchemy(app)
babel = Babel()

def get_locale():
    # Force Finnish for testing
    return 'fi'

babel.init_app(app, locale_selector=get_locale)

app.logger.info(f"BABEL_DEFAULT_LOCALE: {app.config['BABEL_DEFAULT_LOCALE']}")
app.logger.info(f"BABEL_TRANSLATION_DIRECTORIES: {app.config['BABEL_TRANSLATION_DIRECTORIES']}")

# Setup logging
if not os.path.exists('logs'):
    os.mkdir('logs')

log_files = [f'logs/app.log.{i}' for i in range(10)]
for log_file in log_files:
    if not os.path.exists(log_file):
        open(log_file, 'a').close()

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)  # Set to debug level
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.DEBUG)  # Set to debug level
app.logger.info('Application startup')


try:
    from app.models.models import User, Player, GameType, Series, SeriesRegistration, TeamHistory, Game, SingleThrow, SingleRoundThrow, RosterPlayersInSeries
    from app.admin_views import (
        UserAdmin, PlayerAdmin, GameTypeAdmin, SeriesAdmin, 
        SeriesRegistrationAdmin, 
        TeamHistoryAdmin, GameAdmin, RosterAdmin
    )
    from app.utils import custom_gettext
    from app.admin_views.views.game_score_sheet_view import GameScoreSheetAdmin

    admin = Admin(
        app, 
        name=str(_('kyykka kanta hallinta')), 
    )
    
    admin.add_view(UserAdmin(User, db.session, name=_('user'), category='yleinen'))
    admin.add_view(PlayerAdmin(Player, db.session, name=_('player'), category='tiimit'))
    admin.add_view(RosterAdmin(RosterPlayersInSeries, db.session, name=_('team_roster'), category='tiimit'))
    admin.add_view(SeriesRegistrationAdmin(SeriesRegistration, db.session, name=_('registration'), category='sarjat'))
    admin.add_view(TeamHistoryAdmin(TeamHistory, db.session, name=_('team_history'), category='tiimit'))
    admin.add_view(GameTypeAdmin(GameType, db.session, name=_('game_type'), category='yleinen'))
    admin.add_view(SeriesAdmin(Series, db.session, name=_('series'), category='sarjat'))

    admin.add_view(GameAdmin(Game, db.session, name=_('game'),endpoint='game' ))
    admin.add_view(GameScoreSheetAdmin(
        Game, 
        db.session, 
        name=_('game_score_sheet'),
        endpoint='game_score_sheet',  # Must match the endpoint in GameScoreSheetAdmin
        url='/game-score-sheet', category=_('statsit')
    ))

    @app.route('/')
    def index():
        greeting = _('hello_world')  # Use the imported lazy_gettext directly
        app.logger.info(f"Greeting: {greeting}")
        return f"<h1>{str(greeting)}</h1>"  # Convert lazy string to regular string

    if __name__ == '__main__':
        db.create_all()
        app.run(port=int(os.getenv('PORT')))
except Exception as e:
    app.logger.error("Error during application startup", exc_info=e)
    app.logger.error(traceback.format_exc())