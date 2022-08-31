from time import sleep
from utils.functional.base import UtilsBaseFunctionalTest
from selenium.webdriver.common.by import By


class TestAutorsLogin(UtilsBaseFunctionalTest):
    def test_if_user_receive_error_if_the_field_is_empty(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.get_by_xpath("/html/body/main/div[2]/form")
        fields = form.find_elements(By.TAG_NAME, 'input')

        self.fill_form_dummy_data(fields)
        form.find_element(By.TAG_NAME, 'button').click()

        form = self.get_by_xpath("/html/body")
        self.assertIn('Invalid or password', form.text)
    
    def test_if_user_receive_error_if_have_invalid_credentials(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.get_by_xpath("/html/body/main/div[2]/form")

        form.find_element(By.NAME, 'username').send_keys('Robert')
        form.find_element(By.NAME, 'password').send_keys('$tr0ngP@ssw0rd123')

        form.find_element(By.TAG_NAME, 'button').click()
        form = self.get_by_xpath("/html/body")
        self.assertIn('Invalid credentials', form.text)