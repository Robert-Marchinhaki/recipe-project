import pytest
from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


@pytest.mark.fast
@pytest.mark.recipe_test
class RecipesSearchViewsTest(RecipeBaseTest):
    def teste_recipe_search_uses_correct_function(self):
        search = resolve(reverse('recipes:search'))
        self.assertIs(search.func.view_class, views.RecipeListViewSearch)

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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is title one'
        title2 = 'This is title two'

        recipe1 = self.create_recipe(
            title=title1, slug='one', author_data={'username': 'one'})
        recipe2 = self.create_recipe(
            title=title2, slug='two', author_data={'username': 'two'})

        url = reverse('recipes:search')
        response1 = self.client.get(f"{url}?q={title1}")
        response2 = self.client.get(f"{url}?q={title2}")
        response_both = self.client.get(f"{url}?q=this")

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'This is the first recipe'
        description2 = 'This is the second recipe'

        recipe1 = self.create_recipe(
            description=description1, slug='one',
            author_data={'username': 'one'}).description
        recipe2 = self.create_recipe(
            description=description2, slug='two',
            author_data={'username': 'two'}).description

        url = reverse('recipes:search')
        response1 = self.client.get(f"{url}?q={description1}")
        response2 = self.client.get(f"{url}?q={description2}")
        response_both = self.client.get(f"{url}?q=this")

        self.assertIn(recipe1, response1.content.decode('utf-8'))
        self.assertNotIn(recipe1, response2.content.decode('utf-8'))

        self.assertIn(recipe2, response2.content.decode('utf-8'))
        self.assertNotIn(recipe2, response1.content.decode('utf-8'))

        self.assertIn(recipe1, response_both.content.decode('utf-8'))
        self.assertIn(recipe2, response_both.content.decode('utf-8'))
