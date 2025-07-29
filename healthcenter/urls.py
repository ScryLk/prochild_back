from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.AddHealthCenter, name='AddHealthCenter'),
  path("healthcenters/", views.ReturnAllHealthCenters, name="ReturnAllHealthCenters"),
  path("<int:healthcenter_id>", views.GetHealthCenterById, name="GetHealthCenterById"),
  path("delete/<int:healthcenter_id>", views.DeleteHealthCenter, name="DeleteHealthCenter"),
  path("edit/<int:healthcenter_id>/", views.EditHealthCenter, name="EditHealthCenter"),
  path("healthcenters/users/<int:user_id>", views.GetHealthCenterByUsers, name="GetHealthCenterByUsers")
]
  