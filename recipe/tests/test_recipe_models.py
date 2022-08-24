from django.core.exceptions import ValidationError
from parameterized import parameterized
import pytest
from .test_base_recipe import RecipeBaseTest


@pytest.mark.slow
@pytest.mark.recipe_test
class ModelsRecipeTeste(RecipeBaseTest):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

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

    def test_recipe_models_recipe_string_representation(self):
        needed = 'Testing representation '
        msg = f'Recipe string representation must be "{needed}" but "{str(self.recipe)}" was received.'     # noqa
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed, msg=msg)
