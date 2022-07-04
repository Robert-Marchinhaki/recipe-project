from django.urls import path
from recipe import views

urlpatterns = [
    path('', views.index),
    path('recipes/<int:id>/', views.recipe),
]
