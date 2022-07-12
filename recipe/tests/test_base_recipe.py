from django.test import TestCase
from recipe.models import Category, Recipe, User


class RecipeBaseTest(TestCase):
    def setUp(self) -> None:
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

        return super().setUp()
