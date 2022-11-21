import os

from django.shortcuts import get_object_or_404, render
from recipe.models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': recipe,
        'detail_page': True
    })
