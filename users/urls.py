from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register, name='Cadastro'),
    path('login/', views.Login, name="Login"),
    path('usuarios/<int:user_id>/', views.GetUserById, name="GetUserById"),  
    path('usuarios/', views.ReturnAllUsers, name="ReturnAllUsers"), 
    path('usuarios/<int:user_id>/delete/', views.DeleteUserById, name="DeleteUserById"), 
    path('reset-password/', views.ResetPassword, name="ResetPassword"), 
    path('set-new-password/', views.SetNewPassword, name="SetNewPassword"),  
    path("usuarios/edit/<int:user_id>", views.EditUser, name="EditUser")
]