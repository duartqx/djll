from cryptography.fernet import Fernet
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..serializers import LoginSerializer


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        reject = Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]  # pyright: ignore
        password = serializer.validated_data["password"]  # pyright: ignore
        enc = serializer.validated_data.pop("enc", None)  # pyright: ignore

        if enc:
            encryption_key = request.session.get("encryption_key")
            if not encryption_key:
                return reject
            fernet = Fernet(encryption_key.encode())
            email = fernet.decrypt(email).decode()
            password = fernet.decrypt(password).decode()

        user = authenticate(
            request,
            username=email,
            password=password,
        )
        if user is not None:
            login(request, user)
            return Response(
                {"message": "Login successful"}, status=status.HTTP_200_OK
            )
        return reject


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
        csrf = get_token(request)
        if request.session.get("encryption_key") is not None:
            return Response(
                {
                    "enckey": request.session["encryption_key"],
                    "csrf": csrf
                },
                status=200
            )
        encryption_key = Fernet.generate_key().decode()
        request.session["encryption_key"] = encryption_key
        return Response(
            {
                "enckey": encryption_key,
                "csrf": csrf
            },
            status=200
        )
