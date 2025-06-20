from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register, name='Cadastro'),
    path('login/', views.CustomLoginView.as_view(), name="LoginJWT"),  
    path('<int:user_id>/', views.GetUserById, name="GetUserById"),  
    path('', views.ReturnAllUsers, name="ReturnAllUsers"), 
    path('delete/<int:user_id>/', views.DeleteUserById, name="DeleteUserById"), 
    path('reset-password/', views.ResetPassword, name="ResetPassword"), 
    path('set-new-password/', views.SetNewPassword, name="SetNewPassword"),  
    path("edit/<int:user_id>", views.EditUser, name="EditUser"),
]