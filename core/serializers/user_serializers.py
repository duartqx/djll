from rest_framework.serializers import ModelSerializer
from rest_framework.views import Response

from core.models import User


class SelfSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups"]
        read_only_fields = (
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        required_fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }


class ChangePasswordSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["password"]
        required_fields = ["password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


