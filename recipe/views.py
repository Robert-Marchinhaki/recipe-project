from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'recipe/pages/index.html')


def recipe(request, id):
    return render(request, 'recipe/pages/recipe-view.html')
