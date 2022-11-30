import os

from django.db.models import Q
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView
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


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipe/pages/index.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_lst = recipes.object_list.values()

        return JsonResponse(
            list(recipes_lst),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipe/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, category_id=None, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category_id=self.kwargs.get('category_id'),
        )

        if not qs:
            raise Http404()

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipe/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search = self.request.GET.get('q', '').strip()

        if not search:
            raise Http404()

        qs = qs.filter(
            Q(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            ),
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        search = self.request.GET.get('q', '').strip()
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'page_title': f'Buscado por "{search}"',
            'search_term': search,
            'additional_query_url': f'&q={search}'
        })
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'detail_page': True
        })

        return ctx
