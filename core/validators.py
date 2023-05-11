"""
The below validators are used throughout the system to ensure that the data being captured is
valid and 'clean'. They are all pre-compiled regular expressions. (https://www.debuggex.com/?flavor=python)
They can be applied to model fields and form fields.
"""
from django.core.validators import RegexValidator

telephone_number_pattern = "^(0){1}([1-9]){1}([0-9]){8}$"
telephone_number_validator = [
    RegexValidator(
        regex=telephone_number_pattern,
        message='Please enter a valid telephone number; e.g.: "0878205058".'
    )
]