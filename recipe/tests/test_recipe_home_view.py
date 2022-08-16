from unittest.mock import patch

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

    # this part of the test is for testing pagination
    def test_recipe_home_pagination_loads_right_recipe_qty_per_page(self):
        # this test require four recipes or more to work.

        self.create_recipes_to_test_pagination(4)  # noqa: E501

        response = self.client.get(reverse('recipes:home') + '?page=1')
        paginator = response.context['recipes']
        paginator_obj_lst = paginator.object_list

        # recipe 1 is not on this page
        self.assertIn(paginator_obj_lst[1].title,
                      response.content.decode('utf-8'))
        self.assertIn(paginator_obj_lst[2].title,
                      response.content.decode('utf-8'))
        self.assertIn(paginator_obj_lst[3].title,
                      response.content.decode('utf-8'))

    @patch('recipe.views.PER_PAGE', new=3)
    def test_recipe_home_pagination_have_right_qty_the_num_pages(self):
        self.create_recipes_to_test_pagination(7)
        response = self.client.get(reverse('recipes:home'))
        paginator = response.context['recipes'].paginator

        self.assertEqual(paginator.num_pages, 3)

    def test_recipe_home_pagination_has_other_pages(self):
        self.create_recipes_to_test_pagination(4)

        with patch('recipe.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            context = response.context['recipes']

            # test qty page exists
            self.assertEqual(context.has_other_pages(), True)
