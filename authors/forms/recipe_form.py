from django import forms
from recipe.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
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
