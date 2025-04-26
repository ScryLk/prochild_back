from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.AddCategories, name="AddCategories"),
  path('categories/', views.GetAllCategories, name='GetAllCategories'),
  path('delete/<int:categories_id>', views.DeleteCategories, name="DeleteCategories"),
  path("edit/<int:categories_id>", views.EditCategories, name="EditCategories")
]
