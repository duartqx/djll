from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from core.service.alert.alertmessage import AlertMessage
from core.views.auth import LoginView, LogoutView


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

    def http_method_not_allowed(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_alert_manager(self):
        return self.alert_manager(self.request.session)

    @method_decorator(csrf_protect)
    def login(self, *args, **kwargs):
        if self.get_serializer().login():
            return HttpResponseRedirect(reverse("index"))

        ctx = self.get_alert_manager().something_went_wrong()

        return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")


class LogoutHtmxView(LogoutView, TemplateView):
    template_name = "forms/logout.html"
    alert_manager = AlertMessage

    def get_alert_manager(self):
        return self.alert_manager(self.request.session)

    @method_decorator(csrf_protect)
    def logout(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            ctx = self.get_alert_manager().you_are_not_authenticated()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")

        super().logout(self.request, *args, **kwargs)

        ctx = self.get_alert_manager().logout()
        return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")

