from time import sleep

import pytest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from utils.functional.base import UtilsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(UtilsBaseFunctionalTest):
    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field must not be empty'),
        ('email', 'Informe um endereço de email válido.'),
        ('password', 'Password and password2 must be equal'),
        ('password-empty-error', 'Password is required'),
    ])
    def test_empty_first_name_error_message(self, field, value):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_by_xpath("/html/body/main/div[2]/form")
        fields = form.find_elements(By.TAG_NAME, 'input')

        self.fill_form_dummy_data(fields, first_name=' ', last_name=' ', username=' ', chars_qty_repetiton=10, email='dummy@email', password=' ', password2=' ')

        if field == 'password':
            form.find_element(By.NAME, 'password').send_keys(
                '$tr0ngP@ssw0rd123')
            form.find_element(By.NAME, 'password2').send_keys(
                '$tr0ngP@ssw0rd1234')

        form.find_element(By.TAG_NAME, 'button').click()

        form = self.get_by_xpath("/html/body/main/div[2]/form")
        self.assertIn(value, form.text)
