from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from ..service.alert.alertmessage import AlertMessage
from ..service.http.redirect import RedirectWithCtxService
from ..views.auth import LoginView
from ..views.user import ChangePasswordView, CreateUserView, UserView


class GetRedirecToIndexMixin:
    template_name = ""
    alert_manager = AlertMessage

    def get(self, request, *args, **kwargs):
        ctx = request.GET.get("ctx", "")

        if request.user.is_authenticated:
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")

        return render(
            request,
            self.template_name,
            self.alert_manager(request.session).decrypt_ctx(ctx)
            if ctx
            else {},
        )


class IndexView(TemplateView):
    template_name = "index.html"
    alert_manager = AlertMessage

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            ctx = request.GET.get("ctx", "")
            return HttpResponseRedirect(reverse("login") + f"?ctx={ctx}")
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get("ctx"):
            context.update(
                self.alert_manager(request.session).decrypt_ctx(
                    request.GET.get("ctx")
                )
            )
        return self.render_to_response(context)


class LoginHtmxView(GetRedirecToIndexMixin, LoginView):
    template_name = "forms/login.html"
    alert_manager = AlertMessage

    def get_alert_manager(self):
        return self.alert_manager(self.request.session)

    @method_decorator(csrf_protect)
    def login(self, *args, **kwargs):
        if self.get_serializer().login():
            return HttpResponseRedirect(reverse("index"))
        ctx = self.get_alert_manager().something_went_wrong()
        return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")


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
