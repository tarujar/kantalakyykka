from wtforms import StringField, ValidationError
from flask_babel import lazy_gettext as _
import logging
from app.models.models import ThrowType  # Import ThrowType from models

def convert_throw_type_to_str(throw_type):
    """Convert throw_type to string."""
    return throw_type if isinstance(throw_type, str) else throw_type.name

class ThrowInputField(StringField):
    """
    Custom field for inputting throw data
    The field accepts the following input:
    - Valid score: -40 to 80 throw_type is 'VALID'
    - Fault: 'F' value is 0, throw_type is 'FAULT'
    - Hauki: 'H' value is 0, throw_type is 'HAUKI'
    - unused-throw: 'E' or '' value is 1, throw_type is 'E'
    """
    
    def process_formdata(self, valuelist):
        """Process data coming from the form (user input)"""
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Processing throw input field: {valuelist}")
        
        if not valuelist:
            self.data = None
            self.throw_type = ThrowType.E
            self.throw_score = 0
            return

        value = valuelist[0].strip().upper() if valuelist[0] else ''
        self.logger.debug(f"Processing value: {value}")

        # Store the original input value
        self.data = value

        # Process the value and set throw_type and throw_score
        if not value or value == 'E':
            self.throw_type = ThrowType.E
            self.throw_score = 0
        elif value == 'H':
            self.throw_type = ThrowType.HAUKI
            self.throw_score = 0
        elif value == 'F':
            self.throw_type = ThrowType.FAULT
            self.throw_score = 0
        else:
            try:
                score = int(value)
                if -40 <= score <= 80:
                    self.throw_type = ThrowType.VALID
                    self.throw_score = score
                else:
                    raise ValidationError(_('Score must be between -40 and 80'))
            except ValueError:
                self.logger.error(f"Invalid throw input: {value}")
                raise ValidationError(_('Invalid input. Use a score, H (hauki), F (fault), or E (unused)'))

    @staticmethod
    def convert_to_display_value(throw_obj):
        """Convert a SingleThrow object or throw type to display value (H, F, E, or score)"""
        if not throw_obj:
            return ''
        
        # If it's already a string value, return it
        if isinstance(throw_obj, str):
            return throw_obj

        # Get the throw type (either from object or direct enum)
        throw_type = throw_obj.throw_type if hasattr(throw_obj, 'throw_type') else throw_obj
        
        if throw_type == ThrowType.VALID:
            return str(throw_obj.throw_score if hasattr(throw_obj, 'throw_score') else 0)
        elif throw_type == ThrowType.HAUKI:
            return 'H'
        elif throw_type == ThrowType.FAULT:
            return 'F'
        elif throw_type == ThrowType.E:
            return 'E'
        return ''

    def set_throw_display_value(self, throw_obj):
        """Set the field's display value from a SingleThrow object."""
        self.data = self.convert_to_display_value(throw_obj)
