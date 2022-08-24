from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_if_error_message_is_displayed_if_there_are_no_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi publicada ou aprovada.', body.text)
    
    def test_if_user_can_search_the_correct_recipe_by_title(self):
        self.create_n_recipes()
        # first: User open the browser and enter in the page
        self.browser.get(self.live_server_url)
        
        # second: User see the search input saying "Search recipes here"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search recipes here"]'
        )

        # third: User click in the input, write the title of recipe
        # to search the recipe that has this title and press enter key.

        search_input.send_keys('This is a title 1')
        search_input.send_keys(Keys.ENTER)

        sleep(5)