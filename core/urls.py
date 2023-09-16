from django.urls import path
from django.views.generic import TemplateView
from core.views.login_views import LogoutView

from core.views.user_views import ChangePasswordView, CreateUserView

from .views import LoginView, SelfView, UserView

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
        "self/",
        SelfView.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "patch": "update",
            }
        ),
        name="self",
    ),
    path(
        "user/", CreateUserView.as_view({"post": "create"}), name="user_create"
    ),
    path(
        "user/<pk>",
        UserView.as_view({"get": "retrieve"}),
        name="user_retrieve",
    ),
]
