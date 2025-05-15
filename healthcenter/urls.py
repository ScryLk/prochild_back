from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.AddHealthCenter, name='AddHealthCenter'),
  path("healthcenter/", views.ReturnAllHealthCenters, name="ReturnAllHealthCenters")
]
