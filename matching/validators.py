from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.deconstruct import deconstructible
from jsonschema import validate, ValidationError as SchemaValidationError


@deconstructible
class ListOfStringsValidator:
    def __init__(
            self,
            message_invalid_json,
            field_name='this field',
            choices=None,
            min_items=None
    ):
        self.message_invalid_json = message_invalid_json
        self.field_name = field_name
        self.choices_init = choices
        self.min_items = min_items

        self.schema = {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": r"\S"
            },
            "uniqueItems": True
        }
        if min_items:
            self.schema['minItems'] = min_items

        if choices:
            if isinstance(choices[0], str):
                self.choices = set(choices)
            else:
                self.choices = set(choice[0] for choice in choices)
        else:
            self.choices = None

    def __call__(self, obj):
        try:
            validate(obj, schema=self.schema)
            if self.choices:
                for x in obj:
                    if x not in self.choices:
                        raise DjangoValidationError(
                            f'Your choice "{x}" is not one of the allowed choices in {self.field_name}.'
                        )
        except SchemaValidationError:
            raise DjangoValidationError(self.message_invalid_json)

    def __eq__(self, other):
        return (
            isinstance(other, ListOfStringsValidator) and
            self.message_invalid_json == other.message_invalid_json and
            self.field_name == other.field_name and
            self.min_items == other.min_items and
            all(x == y for x, y in zip(self.choices_init, other.choices_init))
        )
