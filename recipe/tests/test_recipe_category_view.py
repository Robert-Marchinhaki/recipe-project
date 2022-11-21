import pytest
from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


@pytest.mark.fast
@pytest.mark.recipe_test
class RecipesCategoryViewsTest(RecipeBaseTest):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 99})
        ).status_code
        self.assertEqual(response, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        # need a recipe for this test
        self.create_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        # Testing if the title was rendered
        self.assertIn(needed_title, content)

    def test_recipe_category_is_published_isnt_true(self):
        # need a recipe for this test
        recipe = self.create_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={'id': recipe.category.id}))

        # Testing if the title was rendered
        self.assertEqual(response.status_code, 404)
