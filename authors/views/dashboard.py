from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipe.models import Recipe
from utils.clear_str import cleaning_str


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            pk=id,
        ).first()

        if not recipe:
            raise Http404()

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            # Now form is valid and you can try save
            recipe = form.save(commit=False)    # Fake save

            recipe.author = request.user
            recipe.preparation_step_is_html = False
            recipe.is_published = False

            form.save()

            messages.success(request, "You edited your recipe with success!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

        return render(
            request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            },
        )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        },
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    recipe = Recipe

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)    # Fake save

        recipe.author = request.user
        recipe.slug = cleaning_str(recipe.title)
        recipe.preparation_step_is_html = False
        recipe.is_published = False

        form.save()

        messages.success(request, "You create your recipe with success!")
        return redirect(
            reverse(
                "authors:dashboard_recipe_edit",
                args=(recipe.id,)
            )
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        },
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, "Recipe deleted with success.")

    return redirect(reverse("authors:dashboard"))
