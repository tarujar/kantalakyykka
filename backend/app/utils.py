from app.main import db, app
from app.models.models import GameType, Series
from flask_babel import gettext as _
import logging

def get_game_type_choices():
    with app.app_context():
        choices = [(gt.id, gt.name) for gt in db.session.query(GameType).all()]
        default = next((gt.id for gt in db.session.query(GameType).all() if gt.name == "Joukkue"), None)
    return choices, default

def get_series_choices():
    """Returns a list of tuples containing (id, display_name) for all series,
    where display_name is formatted as 'name (year)'"""
    with app.app_context():
        series_list = db.session.query(Series).order_by(Series.year.desc(), Series.name).all()
        choices = [(s.id, f"{s.name} ({s.year})") for s in series_list]
        # Default to the most recent series if any exist
        default = choices[0][0] if choices else None
    return choices, default

def custom_gettext(key):
    try:
        with app.app_context():
            translation = str(_(key))
            logging.info(f"Translation attempt - Key: '{key}', Result: '{translation}'")
            return translation
    except Exception as e:
        logging.error(f"Translation error for key '{key}': {e}")
        return key

logging.info("Translation files loaded successfully")
