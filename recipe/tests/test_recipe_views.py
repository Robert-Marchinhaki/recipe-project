from django.test import TestCase
from django.urls import resolve, reverse
from recipe import views
from recipe.models import Category, Recipe, User


class RecipesViewsTest(TestCase):
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

    def test_recipe_home_view_no_have_recipes(self):
        response = self.client.get(
            reverse('recipes:home')).content.decode('utf-8')
        self.assertIn('id="dont-have-recipe"', response)

    def test_recipe_home_template_loads_recipe(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='name',
            last_name='lastname',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe description',
            slug='Slug field',
            preparation_time=2,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='pessoas',
            preparation_step='Passos para fazer a receita',
            preparation_step_is_html=False,
            is_published=True,
            cover='https://thumbs.dreamstime.com/z/etiqueta-adesiva-do-s%C3%ADmbolo-logotipo-circular-da-linguagem-de-programa%C3%A7%C3%A3o-python-colocada-em-um-teclado-laptop-vista-cima-211691587.jpg'  # noqa: E501
        )

        response = self.client.get(reverse('recipes:home'))
        created_recipes = response.context['recipes']
        context = response.context['recipes'].first()
        content = response.content.decode('utf-8')

        # asserções
        self.assertIn(context.author.first_name, content)
        self.assertIn(context.author.last_name, content)
        self.assertIn(context.title, content)
        self.assertEqual(len(created_recipes), 1)   # uma receita

        pass

    # category test
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 99})
        ).status_code
        self.assertEqual(response, 404)

    # detail test
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})).status_code
        self.assertEqual(response, 404)
