from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.test_func_pagination import make_pagination_range

from .models import Recipe


def index(request):
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 9))
    except ValueError:
        current_page = 1
    pagination = Paginator(recipe, 3)
    pag_get_page = pagination.get_page(current_page)

    pagination_range = make_pagination_range(
        pagination.page_range,
        4,
        current_page,
    )

    return render(request, 'recipe/pages/index.html', context={
        'recipes': pag_get_page,
        'pagination_range': pagination_range
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
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': recipe,
        'detail_page': True
    })


def search(request):
    search = request.GET.get('q', '').strip()
    if not search:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        ),
        is_published=True
    ).order_by('-id')

    return render(request, 'recipe/pages/search.html', context={
        'page_title': f'Buscado por "{search}"',
        'search_term': search,
        'recipes': recipes,
    })
