import os

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from recipe.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def theory(request):
    recipes = Recipe.objects.all()
    # recipes = recipes.filter(title__icontains='fugit')

    ctx = {
        'recipes': recipes,
    }

    return render(
        request,
        'recipe/pages/theory.html',
        context=ctx
    )


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
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
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


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipe/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
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
        qs = qs.select_related('author', 'category')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'detail_page': True
        })

        return ctx


class RecipeDetailViewApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.created_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]

        del recipe_dict['is_published']
        del recipe_dict['preparation_step_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
