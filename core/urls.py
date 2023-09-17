from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ChangePasswordView,
    CreateUserView,
    LoginView,
    LogoutView,
    UserView,
    TokensView,
)

template_routes = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path(
        "login/",
        TemplateView.as_view(template_name="forms/login.html"),
        name="loginform",
    ),
    path(
        "user/create/",
        TemplateView.as_view(template_name="forms/user_create.html"),
        name="user_create_form",
    ),
    path(
        "user/edit/",
        TemplateView.as_view(template_name="forms/user_edit.html"),
        name="user_edit_form",
    ),
    path(
        "user/delete/",
        TemplateView.as_view(template_name="forms/user_delete.html"),
        name="user_delete_form",
    ),
]

api_routes = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/password/",
        ChangePasswordView.as_view({"patch": "partial_update"}),
        name="password",
    ),
    path(
        "api/user/",
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
        "api/user/create/",
        CreateUserView.as_view({"post": "create"}),
        name="createuser",
    ),
    path(
        "api/tokens/",
        TokensView.as_view(),
        name="tokens"
    )
]

urlpatterns = template_routes + api_routes
