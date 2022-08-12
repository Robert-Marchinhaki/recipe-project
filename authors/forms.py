from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'Please enter a valid email.'
        }
        error_messages = {
            'username': {
                'required': 'This field is required',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name here'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Type your email here'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            }),
        }