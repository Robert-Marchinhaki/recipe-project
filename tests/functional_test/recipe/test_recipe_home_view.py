from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.functional.base import UtilsBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(UtilsBaseFunctionalTest):
    def test_if_error_message_is_displayed_if_there_are_no_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi publicada ou aprovada.', body.text)

    def test_if_user_can_search_the_correct_recipe_by_title(self):
        self.create_n_recipes()
        # first: User open the browser and enter in the page
        self.browser.get(self.live_server_url)

        # second: User see the search input saying "Search recipes here"
        search_input = self.get_by_xpath(
            '//input[@placeholder="Search recipes here"]')

        # third: User click in the input, write the title of recipe
        # to search the recipe that has this title and press enter key.
        user_search_by = 'This is a title 1'
        search_input.send_keys(user_search_by)
        search_input.send_keys(Keys.ENTER)

        # user found the recipe
        self.assertIn(
            user_search_by,
            self.browser.find_element(By.CLASS_NAME, 'recipe').text
        )

    @patch('recipe.views.PER_PAGE', new=2)
    def test_if_recipe_pagination_is_working(self):
        self.create_n_recipes()

        # first: User open the browser and enter in the page
        self.browser.get(self.live_server_url)

        # User going to the pagination and click in the page 2
        pagination = self.get_by_xpath('//a[@aria-label="Go to page 2"]')
        pagination.click()

        # user can see others recipes
        self.assertEqual(
            2, len(self.browser.find_elements(By.CLASS_NAME, 'recipe')))
