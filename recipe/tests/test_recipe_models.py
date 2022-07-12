from django.core.exceptions import ValidationError

from .test_base_recipe import RecipeBaseTest


class ModelsRecipeTeste(RecipeBaseTest):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

    def test_raises_error_if_title_have_more_65_chars(self):
        self.recipe.title = 'A' * 64

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
