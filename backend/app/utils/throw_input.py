from wtforms import StringField, ValidationError
from flask_babel import lazy_gettext as _
import logging
from app.models.models import ThrowType  # Import ThrowType from models

def convert_throw_type_to_str(throw_type):
    """Convert throw_type to string."""
    return throw_type if isinstance(throw_type, str) else throw_type.name

class ThrowInputField(StringField):
    """Custom field for inputting throw data
    The field accepts the following input:
    - Valid score: -40 to 80 throw_type is 'VALID'
    - Fault: 'F' value is 0, throw_type is 'FAULT'
    - Hauki: 'H' value is 0, throw_type is 'HAUKI'
    - unused-throw: 'E' or '' value is 1, throw_type is 'E'
    """
    def process_formdata(self, valuelist):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"ThrowInputField: value: {valuelist}")

        if not valuelist or not valuelist[0]:
            valuelist = ['E']  # Treat empty fields as "E"

        value = valuelist[0].strip().upper()  # Normalize to uppercase

        switcher = {
            '': (ThrowType.E.value, 1),
            'H': (ThrowType.HAUKI.value, 0),
            'F': (ThrowType.FAULT.value, 0),
            'E': (ThrowType.E.value, 1)
        }

        if value in switcher:
            self.throw_type, self.throw_score = switcher[value]
            self.logger.debug(f"ThrowInputField: {value}, setting throw_type to {self.throw_type} and throw_score to {self.throw_score}")
            return

        try:
            score = int(value)
            if -40 <= score <= 80:
                self.throw_type = ThrowType.VALID.value
                self.throw_score = score
                self.logger.debug(f"ThrowInputField: Valid score, setting throw_type to 'VALID' and throw_score to {score}")
            else:
                raise ValidationError(_('Score must be between -40 and 80'))
        except ValueError:
            raise ValidationError(_('Invalid input. Use a score, H (hauki), F (fault), or E (unused)'))

    @staticmethod
    def get_throw_value(throw=''):
        """Get the value for the throw input field based on throw type"""
        if throw:
            # Ensure throw.throw_type is converted to ThrowType enum
            throw_type_enum = ThrowType(convert_throw_type_to_str(throw.throw_type).upper())

            if throw_type_enum == ThrowType.VALID:
                return throw.throw_score
            else:
                return throw_type_enum.name[0]  # Return the first letter of the throw type (H, F, E)
        logging.error("No throw to render: {throw}")
        return None
