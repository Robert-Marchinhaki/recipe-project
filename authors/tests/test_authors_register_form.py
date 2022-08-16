from authors.forms import RegisterForm
from django.test import TestCase
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
        pass