from authors.forms import RegisterForm
from unittest import TestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: Michael'),
        ('last_name', 'Ex.: bown'),
        ('username', 'Ex.: michael_bown'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_if_the_placeholders_are_correct(self, field, placeholder_val):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_val, placeholder)

    @parameterized.expand([
        ('password', 'The length of your password must be greater than 8 and must contain an uppercase letter, a lowercase letter and a numbers.'),
        ('email', 'Please enter a valid email.')
    ])
    def test_if_help_text_is_rendered(self, field, help_text_val):
        form = RegisterForm()
        help_text = form[field].help_text
        self.assertEqual(help_text_val, help_text)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_if_the_labels_are_correct(self, field, placeholder_val):
        form = RegisterForm()
        placeholder = form[field].label
        self.assertEqual(placeholder_val, placeholder)