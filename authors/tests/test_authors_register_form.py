from unittest import TestCase
import pytest
from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


@pytest.mark.authors_test
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
        ('username', 'Username must have letters, numbers or one of those @.+-_. The length should be between 4 and 150 characters.'),
        ('password', 'Password must have at least one uppercase letter, '
                     'one lowercase letter and one number. The length should be '
                     'at least 8 characters.'),
        ('email', 'Please enter a valid email')
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
            'password': '$Test123',
            'password2': '$Test123',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field must not be empty'),
        ('email', 'E-mail is required'),
        ('password', 'Password is required'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error_message = response.context['form'].fields.get(
            field).error_messages['required']

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, error_message)

    def test_username_field_min_length_should_be_3(self):
        self.form_data['username'] = 'An'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error_message = response.context['form'].fields.get(
            'username').error_messages['min_length']
        msg = 'Username must have at least 3 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, error_message)

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error_message = response.context['form'].fields.get(
            'username').error_messages['max_length']
        msg = 'Username must have less than 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, error_message)

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        # The test below verify if the msg doesn't appear if the password is strong
        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and password2 must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        # The test below verify if msg doesn't appear if the password are equal
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_author_create_raises_404_if_no_post_method(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_if_the_email_already_in_use(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_if_the_user_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'password': '$Testuser123',
            'password2': '$Testuser123',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='$Testuser123'
        )

        self.assertTrue(is_authenticated)
