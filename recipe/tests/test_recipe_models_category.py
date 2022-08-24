from django.core.exceptions import ValidationError

from .test_base_recipe import RecipeBaseTest


class ModelsCategoryTest(RecipeBaseTest):
    def setUp(self) -> None:
        self.category = self.create_category(
            name='Testing category'
        )
        return super().setUp()

    def test_recipe_models_category_string_representation(self):
        needed = 'Testing category'
        msg = f'Recipe string representation must be "{needed}" but "{str(self.category)}" was received.'     # noqa
        self.assertEqual(str(self.category), needed, msg=msg)

    def test_recipe_models_category_name_is_greater_than_65_chars(self):
        self.category.name = 'a' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
