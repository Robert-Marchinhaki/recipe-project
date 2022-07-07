from django.http import Http404
from django.shortcuts import get_list_or_404, render
from utils.recipes.factory import make_recipe

from .models import Recipe


def index(request):
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipe/pages/index.html', context={
        'recipes': recipe
    })


def category(request, category_id):
    recipe = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id'))

    return render(request, 'recipe/pages/category.html', context={
        'recipes': recipe,
        'title': f'{recipe[0].category.name} - Category | '
    })


def recipe(request, id):
    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'detail_page': True
    })
