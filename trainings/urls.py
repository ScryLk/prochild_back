from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.AddTrainings, name='AddTrainings'),
  path('trainings/', views.ReturnAllTrainings, name="ReturnAllTrainings"),
  path('delete/<int:training_id>', views.DeleteTraining, name="DeleteTraining"),
  path('edit/<int:training_id>', views.EditTraining, name="EditTraining"),
  path('trainings/<int:training_id>', views.GetTrainingById, name="GetTrainingById"),
  path('trainings/categorie/<int:categorie_id>', views.GetTrainingByCategories, name="GetTrainingByCategorie"),
  path('deleteall/<int:categorie_id>', views.DeleteAllTrainings, name="DeleteAllTrainings")
]
