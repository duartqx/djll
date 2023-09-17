from cryptography.fernet import Fernet
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from ..serializers import (
    SelfSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
)


@method_decorator(csrf_protect, name="dispatch")
class UserView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = SelfSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(csrf_protect, name="dispatch")
class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CreateUserSerializer

    def get_serializer(self, data, *args, **kwargs):
        if data.get("enc"):
            unencrypted_data = {}
            # May raise KeyError exception on key access, this is handled on
            # the create method
            encryption_key = self.request.session["encryption_key"]
            fernet = Fernet(encryption_key.encode())
            for field, value in filter(lambda d: d[0] != "enc", data.items()):
                unencrypted_data[field] = fernet.decrypt(value).decode()
            return super().get_serializer(data=unencrypted_data, *args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except KeyError:
            return Response({ "error": "Unauthorized" }, status=400)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


@method_decorator(csrf_protect, name="dispatch")
class ChangePasswordView(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
        update_session_auth_hash(self.request, self.request.user)
