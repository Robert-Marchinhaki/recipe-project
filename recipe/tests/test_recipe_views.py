from django.test import TestCase
from django.urls import resolve, reverse
from recipe import views


class RecipesViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.index)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_status_code_is_200(self):
        response = self.client.get(reverse('recipes:home')).status_code
        self.assertIs(response, 200)    # self.assertEqual(response, 200)

    def test_recipe_view_index_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipe/pages/index.html')

    def test_recipe_view_index_no_have_recipes(self):
        response = self.client.get(
            reverse('recipes:home')).content.decode('utf-8')

        self.assertIn('id="dont-have-recipe"', response)
        