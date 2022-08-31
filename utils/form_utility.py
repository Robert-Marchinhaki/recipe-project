from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = f'{attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'''
    ^               # must be start with this
    (?=.*[a-z])     # must contain one lowercase letter
    (?=.*[A-Z])     # must contain one uppercase letter
    (?=.*[0-9])     # must contain one number
    (?=.*[$*&@#])   # must contain one special character
    .{8,}           # must be greater than or equal to 8
    $               # must be end this
    ''', re.VERBOSE)

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter, one number and one special character.'
            ' The length should be at least 8 characters.'
        ),
            code='invalid'
        )
