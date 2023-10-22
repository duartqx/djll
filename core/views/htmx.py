from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from rest_framework.exceptions import ValidationError

from ..views.alertmessage import AlertMessage
from ..views.auth import LoginView
from ..views.user import ChangePasswordView, CreateUserView


class GetMixin:
    template_name = ""

    def get(self, request, *args, **kwargs):
        ctx = request.GET.get("ctx", "")
        if request.user.is_authenticated:
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")
        return render(
            request,
            self.template_name,
            AlertMessage(request.session).decrypt_ctx(ctx) if ctx else {},
        )


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            ctx = request.GET.get("ctx", "")
            return HttpResponseRedirect(reverse("login") + f"?ctx={ctx}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get("ctx"):
            context.update(
                AlertMessage(request.session).decrypt_ctx(
                    request.GET.get("ctx")
                )
            )
        return self.render_to_response(context)


class LoginHtmxView(GetMixin, LoginView):
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


class CreateUserHtmxView(GetMixin, CreateUserView):
    template_name = "forms/user_create.html"
    alert_manager = AlertMessage

    def get_alert_manager(self):
        return self.alert_manager(self.request.session)

    @method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            ctx = self.get_alert_manager().successfully_created_account()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")
        except (KeyError, ValidationError):
            ctx = self.get_alert_manager().something_went_wrong()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")


class ChangePasswordHtmxView(GetMixin, ChangePasswordView):
    template_name = "forms/password_change.html"
    alert_manager = AlertMessage

    def get_alert_manager(self):
        return self.alert_manager(self.request.session)

    @method_decorator(csrf_protect)
    def partial_update(self, request, *args, **kwargs):
        try:
            super().partial_update(request, *args, **kwargs)
            ctx = self.get_alert_manager().successfully_changed_password()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")
        except ValidationError:
            ctx = self.get_alert_manager().something_went_wrong()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")
