from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.AddSections, name='AddSections'),
  path('sections/', views.ReturnAllSections, name="ReturnAllSections"),
  path('delete/<int:sections_id>', views.DeleteSections, name="DeleteSections"),
  path('edit/<int:sections_id>', views.EditSections, name="EditSections"),
  path('sections/<int:sections_id>', views.GetSectionsById, name="GetSectionsById")
]
