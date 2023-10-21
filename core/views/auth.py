from django.contrib.auth import logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..service.encryption import EncryptionService
from ..serializers import LoginSerializer


class LoginView(GenericViewSet):
    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(
            data=self.request.data,  # pyright: ignore
            context={"request": self.request},
        )

    @method_decorator(csrf_protect)
    def login(self, request, *args, **kwargs):
        if self.get_serializer().login():
            return Response(
                {"message": "Login successful"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


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
        tokens = EncryptionService(
            request.session, get_token(request)
        ).get_tokens()

        if request.session.get("encryption_key") is not None:
            return Response(tokens, status=200)

        request.session["encryption_key"] = tokens["enckey"]

        return Response(tokens, status=200)
