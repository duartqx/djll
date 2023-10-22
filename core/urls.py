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
from .views.htmx import (
    ChangePasswordHtmxView,
    IndexView,
    LoginHtmxView,
    CreateUserHtmxView,
)

htmx_routes = [
    path("", IndexView.as_view(), name="index"),
    path(
        "login/",
        LoginHtmxView.as_view({"get": "get", "post": "login"}),
        name="login",
    ),
    path(
        "user/create/",
        CreateUserHtmxView.as_view({"get": "get", "post": "create"}),
        name="user_create",
    ),
    path(
        "user/edit/",
        TemplateView.as_view(template_name="forms/user_edit.html"),
        name="user_edit",
    ),
    path(
        "user/delete/",
        TemplateView.as_view(template_name="forms/user_delete.html"),
        name="user_delete",
    ),
    path(
        "user/password/",
        ChangePasswordHtmxView.as_view(
            {"get": "get", "patch": "partial_update"}
        ),
        name="change_password",
    ),
]

api_routes = [
    path("api/login/", LoginView.as_view({"post": "login"}), name="api_login"),
    path("api/logout/", LogoutView.as_view(), name="api_logout"),
    path(
        "api/password/",
        ChangePasswordView.as_view({"patch": "partial_update"}),
        name="api_password",
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
        name="api_user",
    ),
    path(
        "api/user/create/",
        CreateUserView.as_view({"post": "create"}),
        name="api_createuser",
    ),
    path("api/tokens/", TokensView.as_view(), name="api_tokens"),
]

urlpatterns = htmx_routes + api_routes
