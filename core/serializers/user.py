from rest_framework.serializers import ModelSerializer

from ..models import User


class SelfSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
        ]
        read_only_fields = (
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
        )
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }


class CreateUserSerializer(ModelSerializer):
    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        required_fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
