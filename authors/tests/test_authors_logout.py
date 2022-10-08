from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsLogoutTest(TestCase):
    def test_if_raise_error_case_user_try_use_GET_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_if_raise_error_case_user_try_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'another_user'},
            follow=True
        )

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_if_user_can_logout(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'my_user'},
            follow=True
        )

        self.assertIn(
            'You have successfully logged out',
            response.content.decode('utf-8')
        )
