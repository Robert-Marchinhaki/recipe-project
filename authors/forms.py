from django import forms
from django.contrib.auth.models import User

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: Michael')
        add_placeholder(self.fields['last_name'], 'Ex.: bown')
        add_placeholder(self.fields['username'], 'Ex.: michael_bown')
        add_placeholder(self.fields['email'], 'Your e-mail')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput({
            'placeholder': 'Enter a password'
        }),
        error_messages={
            'required': 'This field is required'
        },
        help_text='The length of your password must be greater than 8 and must contain an uppercase letter, a lowercase letter and a numbers'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput({
            'placeholder': 'Repeat your password'
        }),
        error_messages={
            'required': 'This field is required'
        },
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
