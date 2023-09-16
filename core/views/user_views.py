from django.contrib.auth import update_session_auth_hash
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from ..serializers import SelfSerializer, CreateUserSerializer, ChangePasswordSerializer


class SelfView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = SelfSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = SelfSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        User = self.serializer_class.Meta.model
        return get_object_or_404(User, pk=self.kwargs["pk"])


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]


class ChangePasswordView(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def perform_update(self, serializer):
        serializer.save()
        update_session_auth_hash(self.request, self.request.user)
