from cryptography.fernet import Fernet
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..models import User


class ChangePasswordSerializer(ModelSerializer):
    enc = fields.BooleanField(write_only=True, required=False)
    password = fields.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get("enc"):
            request = self.context["request"]
            encryption_key = request.session.get("encryption_key")
            if not encryption_key:
                raise ValidationError("Unauthorized")
            fernet = Fernet(encryption_key.encode())
            attrs["password"] = fernet.decrypt(attrs["password"]).decode()
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["enc", "password"]


class LoginSerializer(ModelSerializer):
    enc = fields.BooleanField(write_only=True, required=False)
    email = fields.CharField(write_only=True, required=True)
    password = fields.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "enc"]
