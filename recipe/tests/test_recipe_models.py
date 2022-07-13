from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_base_recipe import RecipeBaseTest


class ModelsRecipeTeste(RecipeBaseTest):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

    def test_raises_error_if_title_have_more_65_chars(self):
        self.recipe.title = 'A' * 64

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 200),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A')
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
