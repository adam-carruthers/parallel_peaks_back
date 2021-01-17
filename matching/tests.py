from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import list_of_strings_validator


class Test(TestCase):
    def test_list_of_strings_validator(self):
        basic_los = list_of_strings_validator('blah')
        basic_los([])
        basic_los(['a', 'b', 'c'])
        basic_los(['a'])
        with self.assertRaises(ValidationError):
            basic_los(['a', 2])
        with self.assertRaises(ValidationError):
            basic_los({})
        with self.assertRaises(ValidationError):
            basic_los(['a', 'a'])
        with self.assertRaises(ValidationError):
            basic_los([''])
        with self.assertRaises(ValidationError):
            basic_los(['  '])

        min_items_los = list_of_strings_validator('blah', min_items=3)
        min_items_los(['a', 'b', 'c'])
        min_items_los(['a', 'b', 'c', 'd', 'e'])
        with self.assertRaises(ValidationError):
            min_items_los(['a', 'b'])

        choices = (
            ('hi', 'greeting'),
            ('bye', 'farewell')
        )
        choices_los = list_of_strings_validator('blah', choices=choices)
        choices_los([])
        choices_los(['hi'])
        choices_los(['hi', 'bye'])
        with self.assertRaises(ValidationError):
            choices_los(['a', 'b'])
