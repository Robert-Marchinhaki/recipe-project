from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from utils.functional.base import UtilsBaseFunctionalTest

@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(UtilsBaseFunctionalTest):
    def test_empty_first_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        
        form = self.get_by_xpath("/html/body/main/div[2]/form")
        fields = form.find_elements(By.TAG_NAME, 'input')
        
        self.fill_form_dummy_data(fields)
        
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        form.find_element(By.TAG_NAME, 'button').click()

        form = self.get_by_xpath("/html/body/main/div[2]/form")

        self.assertIn('Write your first name', form.text)
