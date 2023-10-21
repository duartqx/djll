from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..service.enckeys import EncryptionService
from ..serializers import LoginSerializer


@method_decorator(csrf_protect, name="dispatch")
class LoginView(GenericViewSet):
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.login():
            return Response(
                {"message": "Login successful"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def htmx_login(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.login():
            return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(f"{reverse('loginform')}?somethingwrong=1")


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {"message": "Logout successful"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@method_decorator(csrf_protect, name="dispatch")
class TokensView(APIView):
    def get(self, request, *args, **kwargs):
        tokens = EncryptionService.get_keys(
            request.session, csrf=get_token(request)
        )

        if request.session.get("encryption_key") is not None:
            return Response(tokens, status=200)

        request.session["encryption_key"] = tokens["enckey"]

        return Response(tokens, status=200)
