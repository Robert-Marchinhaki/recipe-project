from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


class RecipesHomeViewsTest(RecipeBaseTest):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.index)

    def test_recipe_home_view_status_code_is_200(self):
        response = self.client.get(reverse('recipes:home')).status_code
        self.assertEqual(response, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipe/pages/index.html')

    # @skip('WIP')
    def test_recipe_home_view_no_have_recipes(self):
        response = self.client.get(
            reverse('recipes:home')).content.decode('utf-8')
        self.assertIn(
            '<h1>Nenhuma receita foi publicada ou aprovada.</h1>',
            response)

        # self.fail('WIP')

    def test_recipe_home_template_loads_recipes(self):
        # need a recipe for this test
        self.create_recipe()

        response = self.client.get(reverse('recipes:home'))
        context = response.context['recipes']
        content = response.content.decode('utf-8')

        # Testing if the title was rendered
        self.assertIn(context.object_list[0].title, content)

    def test_recipe_home_is_published_isnt_true(self):
        # need a recipe for this test
        self.create_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Testing if the title was rendered
        self.assertIn(
            '<h1>Nenhuma receita foi publicada ou aprovada.</h1>',
            response.content.decode('utf-8'))
