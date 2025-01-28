from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_babel import lazy_gettext as _
from sqlalchemy.exc import IntegrityError, DataError
from flask import flash
import re
from app.utils.display import custom_gettext
from app.utils.validation_messages import handle_integrity_error, handle_data_error

class CustomModelView(ModelView):
    form_base_class = SecureForm
    field_flags = {"requiredif": True}
    name = "Custom Model"

    # Override Flask-Admin's default messages
    def _get_create_success_msg(self):
        return _('creation_successful')

    def _get_edit_success_msg(self):
        return _('save_successful')

    def _get_delete_success_msg(self):
        return _('delete_successful')

    # Override error messages
    def _get_create_error_msg(self):
        return _('creation_failed')

    def _get_edit_error_msg(self):
        return _('save_failed')

    def _get_delete_error_msg(self):
        return _('delete_failed')

    def _refresh_translations(self):
        if hasattr(self, 'column_labels'):
            self.column_labels = {key: custom_gettext(value) for key, value in self.column_labels.items()}
        if hasattr(self, 'form_labels'):
            self.form_labels = {key: custom_gettext(value) for key, value in self.form_labels.items()}
        if hasattr(self, 'form_extra_fields') and self.form_extra_fields:
            for field in self.form_extra_fields.values():
                if hasattr(field, 'label') and hasattr(field.label, 'text'):
                    field.label.text = custom_gettext(field.label.text)

    def __init__(self, model, session, **kwargs):
        self._refresh_translations()
        super().__init__(model, session, **kwargs)

    def render(self, template, **kwargs):
        self._refresh_translations()
        return super().render(template, **kwargs)

    def handle_view_exception(self, exc):
        if isinstance(exc, IntegrityError):
            return handle_integrity_error(exc)
        if isinstance(exc, DataError):
            return handle_data_error(exc)
        return super().handle_view_exception(exc)
