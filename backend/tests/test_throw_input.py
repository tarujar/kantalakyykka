import unittest
from app.utils.throw_input import ThrowInputField, ThrowType

class MockThrow:
    def __init__(self, throw_type, throw_score):
        self.throw_type = throw_type
        self.throw_score = throw_score

class TestThrowInputField(unittest.TestCase):
    def test_get_throw_value_valid(self):
        throw = MockThrow(ThrowType.VALID, 10)
        result = ThrowInputField.get_throw_value(throw)
        self.assertEqual(result, 10)

    def test_get_throw_value_hauki(self):
        throw = MockThrow(ThrowType.HAUKI, 0)
        result = ThrowInputField.get_throw_value(throw)
        self.assertEqual(result, 'H')

    def test_get_throw_value_fault(self):
        throw = MockThrow(ThrowType.FAULT, 0)
        result = ThrowInputField.get_throw_value(throw)
        self.assertEqual(result, 'F')

    def test_get_throw_value_unused(self):
        throw = MockThrow(ThrowType.E, 1)
        result = ThrowInputField.get_throw_value(throw)
        self.assertEqual(result, 'E')

    def test_get_throw_value_empty(self):
        throw = MockThrow(ThrowType.E, '')
        result = ThrowInputField.get_throw_value(throw)
        self.assertEqual(result, 'E')

    def test_get_throw_value_none(self):
        result = ThrowInputField.get_throw_value(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
