from selenium.webdriver.common.by import By
import pytest
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_if_error_message_is_displayed_if_there_are_no_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi publicada ou aprovada.', body.text)
        self.browser.quit()
