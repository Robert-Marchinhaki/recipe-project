import os

from django.views.generic import ListView
from recipe.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipe/pages/index.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pag_get_page, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({
            'recipes': pag_get_page,
            'pagination_range': pagination_range,
        })
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipe/pages/index.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipe/pages/category.html'

    def get_queryset(self, category_id=None, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category_id=self.kwargs.get('category_id'),
            )

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipe/pages/search.html'
