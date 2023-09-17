from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ChangePasswordView,
    CreateUserView,
    LoginView,
    LogoutView,
    UserView,
    GetTokensView,
)

template_routes = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path(
        "login/",
        TemplateView.as_view(template_name="loginform.html"),
        name="loginform",
    ),
    path(
        "user/create/",
        TemplateView.as_view(template_name="createuserform.html"),
        name="createuserform",
    ),
    path(
        "user/edit/",
        TemplateView.as_view(template_name="edituserform.html"),
        name="edituserform",
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
        GetTokensView.as_view(),
        name="tokens"
    )
]

urlpatterns = template_routes + api_routes
