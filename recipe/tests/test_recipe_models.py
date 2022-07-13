from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_base_recipe import Recipe, RecipeBaseTest


class ModelsRecipeTeste(RecipeBaseTest):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

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

    @parameterized.expand([
        ('title', 65),
        ('description', 200),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_step_is_html_default_is_false(self):
        recipe = self.create_recipe_for_test_defaults()
        self.assertFalse(recipe.preparation_step_is_html,
                         msg='preparation_step_is_html is not False')

    def test_recipe_is_published_default_is_false(self):
        recipe = self.create_recipe_for_test_defaults()
        self.assertFalse(recipe.is_published,
                         msg='is_published is not False')
