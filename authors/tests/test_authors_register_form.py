from authors.forms import RegisterForm
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.urls import reverse

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

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': '$0ne$tr0ngPassw0rd',
            'password2': '$0ne$tr0ngPassw0rd',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
