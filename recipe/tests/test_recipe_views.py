from django.urls import resolve, reverse
from recipe import views

from .test_base_recipe import RecipeBaseTest


class RecipesViewsTest(RecipeBaseTest):
    # home test
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
        context = response.context['recipes'].first()
        content = response.content.decode('utf-8')

        # Testing if the title was rendered
        self.assertIn(context.title, content)

    def test_recipe_home_is_published_isnt_true(self):
        # need a recipe for this test
        self.create_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Testing if the title was rendered
        self.assertIn(
            '<h1>Nenhuma receita foi publicada ou aprovada.</h1>',
            response.content.decode('utf-8'))

    # category test
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

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
            reverse('recipes:category', kwargs={'category_id': recipe.category.id}))

        # Testing if the title was rendered
        self.assertEqual(response.status_code, 404)

    # detail test
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

    def teste_recipe_search_uses_correct_function(self):
        search = resolve(reverse('recipes:search'))
        self.assertIs(search.func, views.search)
