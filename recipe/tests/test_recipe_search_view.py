from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


class RecipesSearchViewsTest(RecipeBaseTest):
    def teste_recipe_search_uses_correct_function(self):
        search = resolve(reverse('recipes:search'))
        self.assertIs(search.func, views.search)

    def teste_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipe/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Test'
        response = self.client.get(url)
        self.assertIn('Buscado por &quot;Test&quot;',
                      response.content.decode('utf-8'))
