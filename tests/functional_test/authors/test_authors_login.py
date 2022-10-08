from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from utils.functional.base import UtilsBaseFunctionalTest


class TestAuthorsLogin(UtilsBaseFunctionalTest):
    def test_if_user_receive_error_if_the_field_is_empty(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.get_by_xpath("/html/body/main/div[2]/form")
        fields = form.find_elements(By.TAG_NAME, 'input')

        self.fill_form_dummy_data(fields, username=' ', password=' ')
        form.find_element(By.TAG_NAME, 'button').click()

        form = self.get_by_xpath("/html/body")
        self.assertIn('Invalid username or password',
                      form.text.replace("\n", ' '))

    def test_if_user_receive_error_if_have_invalid_credentials(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.get_by_xpath("/html/body/main/div[2]/form")

        form.find_element(By.NAME, 'username').send_keys('Robert')
        form.find_element(By.NAME, 'password').send_keys('$tr0ngP@ssw0rd123')

        form.find_element(By.TAG_NAME, 'button').click()
        form = self.get_by_xpath("/html/body")
        self.assertIn('Invalid credentials', form.text)

    def test_user_valid_data_can_login_with_sucefully(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser")

        # user open the browser
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see the form
        form = self.get_by_xpath("/html/body/main")

        # User enter with your username and your password
        form.find_element(By.NAME, 'username').send_keys(
            user.username)   # username
        form.find_element(By.NAME, 'password').send_keys(
            'TestUser')   # password

        # User send data
        form.find_element(By.TAG_NAME, 'button').click()
        form = self.get_by_xpath("/html/body")

        self.assertIn(
            f'You are logged in with {user.username}.',
            form.text
        )

    def test_login_create_raise_404_case_request_is_not_POST(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn(
            'not found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
