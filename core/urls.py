from django.urls import path
from django.views.generic import TemplateView
from core.views.login_views import LogoutView

from .views import ChangePasswordView, CreateUserView, LoginView, UserView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password/",
        ChangePasswordView.as_view({"patch": "partial_update"}),
        name="password",
    ),
    path(
        "user/",
        UserView.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
        name="user",
    ),
    path(
        "createuser/",
        CreateUserView.as_view({"post": "create"}),
        name="createuser",
    ),
]
