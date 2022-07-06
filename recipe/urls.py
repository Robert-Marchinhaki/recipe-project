from django.urls import path
from recipe import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='home'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
]
