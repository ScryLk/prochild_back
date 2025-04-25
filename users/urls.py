from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.Cadastro, name='cadastro'),
    path('login/', views.Login, name="login"),
    path('usuarios/<int:user_id>/', views.GetUserById, name="GetUserById"),  
    path('usuarios/', views.ReturnAllUsers, name="ReturnAllUsers"), 
    path('usuarios/<int:user_id>/delete/', views.DeleteUserById, name="DeleteUserById"), 
]