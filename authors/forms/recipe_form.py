from collections import defaultdict

from django import forms
from django.forms import ValidationError
from recipe.models import Recipe
from utils.form_utility import add_attr
from utils.positive_number import get_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_step'), 'class', 'span-2')

    title = forms.CharField(
        min_length=4,
        max_length=65,
        error_messages={
            'min_length': 'The title must have at least 4 chars.',
            'max_length': 'The title must have less than 65 chars',
        },
    )
    description = forms.CharField(
        min_length=4,
        max_length=65,
        error_messages={
            'min_length': 'The description must have at least 4 chars.',
            'max_length': 'The description must have less than 65 chars',
        },
    )

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

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 4:
            self._my_errors['title'].append('Must have at least 4 chars.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not get_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not get_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value
