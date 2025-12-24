from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('result/<int:recipe_id>/', views.result, name='result'),
]
