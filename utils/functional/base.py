from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipe.tests.test_base_recipe import RecipeMixin
from utils.browser import make_chrome_browser


class UtilsBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
