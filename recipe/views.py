from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from .models import Recipe


def index(request):
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')

    cunrrent_page = request.GET.get('page', 1)
    pagination = Paginator(recipe, 2)
    pag_get_page = pagination.get_page(cunrrent_page)

    return render(request, 'recipe/pages/index.html', context={
        'recipes': pag_get_page
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
