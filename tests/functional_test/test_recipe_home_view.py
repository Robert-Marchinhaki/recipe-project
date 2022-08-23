from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):

    def test_if_no_have_recipes(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi publicada ou aprovada.', body.text)
        sleep(5)
        browser.quit()
