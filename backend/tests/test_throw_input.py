import unittest
from app.utils.throw_input import ThrowInputField
from app.models.models import ThrowType
import pytest_asyncio

class MockThrow:
    def __init__(self, throw_type, throw_score):
        self.throw_type = throw_type
        self.throw_score = throw_score

class TestThrowInputField(unittest.TestCase):
    def test_convert_to_display_value_valid(self):  # Renamed method
        throw = MockThrow(ThrowType.VALID, 10)
        result = ThrowInputField.convert_to_display_value(throw)  # Updated method name
        self.assertEqual(result, '10')  # Note: result is string now

    def test_convert_to_display_value_hauki(self):  # Renamed method
        throw = MockThrow(ThrowType.HAUKI, 0)
        result = ThrowInputField.convert_to_display_value(throw)  # Updated method name
        self.assertEqual(result, 'H')

    def test_convert_to_display_value_fault(self):  # Renamed method
        throw = MockThrow(ThrowType.FAULT, 0)
        result = ThrowInputField.convert_to_display_value(throw)  # Updated method name
        self.assertEqual(result, 'F')

    def test_convert_to_display_value_unused(self):  # Renamed method
        throw = MockThrow(ThrowType.E, 1)
        result = ThrowInputField.convert_to_display_value(throw)  # Updated method name
        self.assertEqual(result, 'E')

    def test_convert_to_display_value_none(self):  # Renamed method
        result = ThrowInputField.convert_to_display_value(None)  # Updated method name
        self.assertEqual(result, '')  # Now returns empty string instead of None

if __name__ == '__main__':
    unittest.main()

import pytest
from wtforms import Form
from wtforms.validators import ValidationError
from app.utils.throw_input import ThrowInputField
from app.models.models import ThrowType, SingleThrow

@pytest_asyncio.fixture
def field():
    class TestForm(Form):
        test_field = ThrowInputField('Test')
    form = TestForm()
    return form.test_field

def test_throw_input_field_process_valid_score(field):
    field.process_formdata(['10'])
    assert field.data == '10'
    assert field.throw_type == ThrowType.VALID
    assert field.throw_score == 10

def test_throw_input_field_process_hauki(field):
    field.process_formdata(['H'])
    assert field.data == 'H'
    assert field.throw_type == ThrowType.HAUKI
    assert field.throw_score == 0

def test_throw_input_field_process_fault(field):
    field.process_formdata(['F'])
    assert field.data == 'F'
    assert field.throw_type == ThrowType.FAULT
    assert field.throw_score == 0

def test_throw_input_field_process_empty(field):
    field.process_formdata([''])
    assert field.data == ''
    assert field.throw_type == ThrowType.E
    assert field.throw_score == 0

def test_throw_input_field_invalid_score(field):
    with pytest.raises(ValidationError):
        field.process_formdata(['100'])  # Out of range

def test_throw_input_field_invalid_input(field):
    with pytest.raises(ValidationError):
        field.process_formdata(['X'])  # Invalid character

def test_convert_to_display_value():
    # Test with SingleThrow object
    throw = SingleThrow(throw_type=ThrowType.VALID, throw_score=10)
    assert ThrowInputField.convert_to_display_value(throw) == '10'

    throw = SingleThrow(throw_type=ThrowType.HAUKI, throw_score=0)
    assert ThrowInputField.convert_to_display_value(throw) == 'H'

    # Test with None
    assert ThrowInputField.convert_to_display_value(None) == ''

    # Test with string
    assert ThrowInputField.convert_to_display_value('H') == 'H'

def test_set_throw_display_value(field):
    throw = SingleThrow(throw_type=ThrowType.HAUKI, throw_score=0)
    field.set_throw_display_value(throw)
    assert field.data == 'H'
