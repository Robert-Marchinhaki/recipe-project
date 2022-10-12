from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from recipe.models import Recipe
from utils.clear_str import cleaning_str

from .forms import LoginForm, RegisterForm
from .forms.recipe_form import AuthorRecipeForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        form.save()
        messages.success(
            request, 'Your account has been sucefully created, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')


def login_views(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'You have successfully logged out')
    logout(request)
    return redirect(reverse('authors:login'))


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
def dashboard_recipe_edit(request, id):
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
