from django import forms
from recipe.models import Recipe
from utils.form_utility import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add_attr(self.fields.get('preparation-steps'), 'class', 'span-2')
        # add_attr(self.fields.get('cover'), 'class', 'span-2')
        add_attr(self.fields.get('preparation_step'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_step',
            'cover',
            'category',
        )
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                },
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pessoas', 'Pessoas'),
                    ('Pedaços', 'Pedaços'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }
