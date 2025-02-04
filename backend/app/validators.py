from wtforms.validators import ValidationError
from flask_babel import lazy_gettext as _

def validate_all_throws_not_zero(form, field):
    """Custom validation to ensure all throws are not zero"""
    for team_round_throws in [form.team_1_round_throws, form.team_2_round_throws]:
        for round_throws in team_round_throws:
            for single_throw_form in round_throws.round_1.entries + round_throws.round_2.entries:
                if single_throw_form.throw_1.data == single_throw_form.throw_2.data == single_throw_form.throw_3.data == single_throw_form.throw_4.data == 0:
                    raise ValidationError(_('All throws cannot be zero'))
