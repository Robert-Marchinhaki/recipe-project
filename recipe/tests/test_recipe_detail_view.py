import pytest
from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


@pytest.mark.fast
@pytest.mark.recipe_test
class RecipesDetailViewsTest(RecipeBaseTest):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})).status_code
        self.assertEqual(response, 404)

    def test_recipe_detail_template_loads_recipe(self):
        needed_title = 'This is a detail page - Test if loads one recipe'

        # need a recipe for this test
        self.create_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))

        content = response.content.decode('utf-8')

        # Testing if the title was rendered
        self.assertIn(needed_title, content)

    def test_recipe_detail_is_published_isnt_true(self):
        # need a recipe for this test
        recipe = self.create_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        # Testing if the title was rendered
        self.assertEqual(response.status_code, 404)
