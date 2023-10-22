from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from core.service.http.redirect import RedirectWithCtxService
from core.views.user import ChangePasswordView, CreateUserView, UserView

from .index import GetRedirecToIndexMixin


class CreateUserHtmxView(GetRedirecToIndexMixin, CreateUserView):
    template_name = "forms/user_create.html"
    service = RedirectWithCtxService

    def get_redirect_response_with_ctx(self, request, *args, **kwargs):
        return self.service(
            request,
            super().create,
            "successfully_created_account",
            *args,
            **kwargs,
        ).get_redirect_response()

    @method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):
        return self.get_redirect_response_with_ctx(request, *args, **kwargs)


class ChangePasswordHtmxView(TemplateView, ChangePasswordView):
    template_name = "forms/password_change.html"
    service = RedirectWithCtxService

    def get_redirect_response_with_ctx(self, request, *args, **kwargs):
        return self.service(
            request,
            super().partial_update,
            "successfully_changed_password",
            *args,
            **kwargs,
        ).get_redirect_response()

    @method_decorator(csrf_protect)
    def partial_update(self, request, *args, **kwargs):
        return self.get_redirect_response_with_ctx(request, *args, **kwargs)


class EditUserHtmxView(UserView, TemplateView):
    template_name = "forms/user_edit.html"
    service = RedirectWithCtxService

    def get_redirect_response_with_ctx(self, request, *args, **kwargs):
        return self.service(
            request,
            super().partial_update,
            "successfully_updated_user",
            *args,
            **kwargs,
        ).get_redirect_response()

    @method_decorator(csrf_protect)
    def partial_update(self, request, *args, **kwargs):
        return self.get_redirect_response_with_ctx(request, *args, **kwargs)


class DeleteUserHtmxView(UserView, TemplateView):
    template_name = "forms/user_delete.html"
    service = RedirectWithCtxService

    def get_redirect_response_with_ctx(self, request, *args, **kwargs):
        return self.service(
            request,
            super().destroy,
            "successfully_deleted_user",
            *args,
            **kwargs,
        ).get_redirect_response()

    @method_decorator(csrf_protect)
    def destroy(self, request, *args, **kwargs):
        return self.get_redirect_response_with_ctx(request, *args, **kwargs)
