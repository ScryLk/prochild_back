from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    path("", views.ReturnAllUsers, name="list_users"),
    path("<int:user_id>/", views.GetUserById, name="get_user"),
    path("edit/<int:user_id>/", views.EditUser, name="edit_user"),
    path("delete/<int:user_id>/", views.DeleteUserById, name="delete_user"),

    path("reset-password/", views.ResetPassword, name="reset_password"),
    path("set-new-password/", views.SetNewPassword, name="set_new_password"),
]
