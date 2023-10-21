from django.contrib.auth import authenticate, login
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..service.encryption import EncryptionService
from ..models import User


class ChangePasswordSerializer(ModelSerializer):
    """
    Password PATCH serializer, unencrypts data with Fernet if the 'enc' kwarg
    is True
    """

    enc = fields.BooleanField(write_only=True, required=False)
    password = fields.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        Unencrypt password before validation if 'enc' kwarg is in attrs

        Raises:
            ValidationError
        """
        if attrs.get("enc"):
            enc_service = self.context["encryption_service"]
            attrs["password"] = enc_service.decrypt(attrs["password"])
        return super().validate(attrs)

    def update(self, instance, validated_data):
        """Sets the new password and returns the instance object"""
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["enc", "password"]


class LoginSerializer(ModelSerializer):
    """
    Authentication Login Serializer, unencrypts data on the View before
    validating if enc is True
    """

    enc = fields.BooleanField(write_only=True, required=False)
    email = fields.CharField(write_only=True, required=True)
    password = fields.CharField(write_only=True, required=True)

    def login(self) -> bool:
        self.is_valid(raise_exception=True)

        request = self.context["request"]
        enc_service = self.context["encryption_service"]

        email = self.validated_data["email"]  # pyright: ignore
        password = self.validated_data["password"]  # pyright: ignore
        enc = self.validated_data.pop("enc", None)  # pyright: ignore

        if enc:
            enckey = request.session.get("encryption_key")

            if not enckey:
                return False

            email, password = enc_service.decrypt_list(email, password)

        user = authenticate(
            request,
            username=email,
            password=password,
        )
        if user is not None:
            login(request, user)
            return True
        return False

    class Meta:
        model = User
        fields = ["email", "password", "enc"]
