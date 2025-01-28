from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField
from .base import CustomModelView

class UserAdmin(CustomModelView):
    form_overrides = {
        'email': StringField,
        'hashed_password': PasswordField
    }
    column_labels = {
        'username': _('username'),
        'email': _('email'),
        'hashed_password': _('password'),
        'created_at': _('created_at')
    }
    form_labels = column_labels
    form_columns = ['username', 'email', 'hashed_password', 'created_at']

