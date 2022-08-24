from django.test import TestCase
from recipe.models import Category, Recipe, User


class RecipeBaseTest(TestCase):
    def create_category(self, name='category'):
        return Category.objects.create(name=name)

    def create_author(self, first_name='name', last_name='last_name', username='username', password='123456', email='username@email.com'):  # noqa: E501
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def create_recipe(self, category_data=None, author_data=None, title='Recipe Title', description='Recipe Description', slug='slug-title', preparation_time=0, preparation_time_unit='Minutos', servings=0, servings_unit='pessoas', preparation_step='Step for make recipe', preparation_step_is_html=False, is_published=True, cover=None):   # noqa: E501
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        if cover is None:
            cover = 'https://thumbs.dreamstime.com/z/etiqueta-adesiva-do-s%C3%ADmbolo-logotipo-circular-da-linguagem-de-programa%C3%A7%C3%A3o-python-colocada-em-um-teclado-laptop-vista-cima-211691587.jpg'  # noqa: E501

        return Recipe.objects.create(
            category=self.create_category(**category_data),
            author=self.create_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
            cover=cover
        )

    def create_recipes_to_test_pagination(self, qty_recipes):
        for i in range(qty_recipes):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            recipes = self.create_recipe(**kwargs)
        return recipes

    def create_recipe_for_test_defaults(self):
        cover = 'https://thumbs.dreamstime.com/z/etiqueta-adesiva-do-s%C3%ADmbolo-logotipo-circular-da-linguagem-de-programa%C3%A7%C3%A3o-python-colocada-em-um-teclado-laptop-vista-cima-211691587.jpg'  # noqa: E501
        recipe = Recipe(
            category=self.create_category(name='Category for test default'),
            author=self.create_author(username='newuser'),
            title='Recipe title',
            description='Recipe description',
            slug='slug-test',
            preparation_time=1,
            preparation_time_unit='Minutos',
            servings=1,
            servings_unit='pessoas',
            preparation_step='Passos para preparar a receita',
            cover=cover
        )
        self.recipe.full_clean()
        self.recipe.save()
        return recipe
