from django.shortcuts import render
from utils.recipes.factory import make_recipe

from .models import Recipe


def index(request):
    recipe = Recipe.objects.all().order_by('-id')
    return render(request, 'recipe/pages/index.html', context={
        'recipes': recipe
    })


def category(request, category_id):
    recipe = Recipe.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'recipe/pages/index.html', context={
        'recipes': recipe
    })


def recipe(request, id):
    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'detail_page': True
    })
