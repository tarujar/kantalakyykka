from wtforms import StringField, ValidationError
from flask_babel import lazy_gettext as _

class ThrowInputField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0].strip().lower()
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                score = int(value)
                if -80 <= score <= 20:
                    self.throw_type = 'valid'
                    self.throw_score = score
                else:
                    raise ValidationError(_('Invalid score value'))
            elif value in ['h', 'e', 'f']:
                self.throw_type = 'fault' if value == 'f' else 'hauki' if value == 'h' else 'valid'
                self.throw_score = 0 if value in ['h', 'f'] else 1
            else:
                raise ValidationError(_('Invalid input value'))
        else:
            raise ValidationError(_('Input required'))
