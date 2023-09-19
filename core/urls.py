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
    IndexView,
    UserDeleteHtmxView,
    UserEditHtmxView,
    UserCreateHtmxView,
    PasswordChangeHtmxView,
)

htmx_routes = [
    path("", IndexView.as_view(), name="index"),
    path(
        "login/",
        TemplateView.as_view(template_name="forms/login.html"),
        name="loginform",
    ),
    path(
        "user/create/",
        UserCreateHtmxView.as_view(),
        name="user_create_form",
    ),
    path("user/edit/", UserEditHtmxView.as_view(), name="user_edit_form"),
    path("user/delete/", UserDeleteHtmxView.as_view(), name="user_delete_form"),
    path(
        "user/password/",
        PasswordChangeHtmxView.as_view(),
        name="change_password_form",
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
    path("api/tokens/", TokensView.as_view(), name="tokens"),
]

urlpatterns = htmx_routes + api_routes
