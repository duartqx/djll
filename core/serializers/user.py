from rest_framework.serializers import ModelSerializer

from ..models import User


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