from cryptography.fernet import Fernet
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import HttpResponseRedirect
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from typing import Any, Dict

from ..serializers import (
    SelfSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
)


def unencrypt_data(data, encryption_key) -> Dict[str, Any]:
    """Decodes data using Fernet with the encryption_key passed as argument"""
    if data.get("enc"):
        unencrypted_data = {}
        fernet = Fernet(encryption_key.encode())
        for field, value in filter(lambda d: d[0] != "enc", data.items()):
            unencrypted_data[field] = fernet.decrypt(value).decode()
        return unencrypted_data
    return data


@method_decorator(csrf_protect, name="dispatch")
class UserView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    View for User GET, PATCH and DELETE HTTP requests
    """

    serializer_class = SelfSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        """
        Returns the instantiated Serializer class

        Raises:
            KeyError
        """
        data = kwargs.pop("data", {})
        # May raise KeyError exception on key access, this is handled on
        # the create method
        return super().get_serializer(
            data=unencrypt_data(data, self.request.session["encryption_key"]),
            *args,
            **kwargs,
        )

    def update(self, request, *args, **kwargs):
        """
        Tries to update, but if it fails because of missing encryption_key
        in self.request.session it'll return a status 400 instead
        """
        try:
            return super().update(request, *args, **kwargs)
        except KeyError:
            return Response({"error": "Unauthorized"}, status=400)


@method_decorator(csrf_protect, name="dispatch")
class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    """View for User POST"""

    serializer_class = CreateUserSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Returns the instantiated Serializer class

        Raises:
            KeyError
        """
        data = kwargs.pop("data", {})
        # May raise KeyError exception on key access, this is handled on
        # the create method
        return super().get_serializer(
            data=unencrypt_data(data, self.request.session["encryption_key"]),
            *args,
            **kwargs,
        )

    def create(self, request, *args, **kwargs):
        """
        Tries to create, but if it fails because of missing encryption_key
        in self.request.session it'll return a status 400 instead
        """
        try:
            return super().create(request, *args, **kwargs)
        except KeyError:
            return Response({"error": "Unauthorized"}, status=400)


@method_decorator(csrf_protect, name="dispatch")
class ChangePasswordView(mixins.UpdateModelMixin, GenericViewSet):
    """View for password PATCH"""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
        update_session_auth_hash(self.request, self.request.user)
