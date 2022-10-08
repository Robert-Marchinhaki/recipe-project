from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.form_utility import add_placeholder, strong_password


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
            'min_length': 'Username must have at least 3 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=3, max_length=150,
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
        validators=[strong_password]
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password2 is required'
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        all_data = super().clean()

        password = all_data.get('password')
        password2 = all_data.get('password2')
        if password != password2:
            raise ValidationError({
                'password': [
                    'Password and password2 must be equal',
                ],
                'password2': [
                    'Password and password2 must be equal',
                ],
            })

        return all_data
