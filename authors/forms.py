import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: Michael')
        add_placeholder(self.fields['last_name'], 'Ex.: bown')
        add_placeholder(self.fields['username'], 'Ex.: michael_bown')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Write your first name',
        }
    )
    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Write your last name',
        }
    )
    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'required': 'E-mail is required',
        },
        help_text='Please enter a valid email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password is required'
        },
        help_text='The length of your password must be greater than 8 and must contain an uppercase letter, a lowercase letter and a numbers.',
        validators=[strong_password]
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password'
        },
        validators=[strong_password]
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    def clean(self):
        all_data = super().clean()

        password = all_data.get('password')
        password2 = all_data.get('password2')
        pw_validation_error = ValidationError(
            'passwords do not match.',
            code='invalid',
        )
        if password != password2:
            raise ValidationError({
                'password': [
                    'Password and password2 must be equal.',
                    pw_validation_error,
                ],
                'password2': [
                    'Password and password2 must be equal.',
                    pw_validation_error,
                ],
            })

        return all_data
