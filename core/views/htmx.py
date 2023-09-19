from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("loginform"))
        return super().dispatch(request, *args, **kwargs)


class UserCreateHtmxView(TemplateView):
    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["forms/partials/_partial_user_create.html"]
        return ["forms/user_create.html"]


class UserDeleteHtmxView(TemplateView):
    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["forms/partials/_partial_user_delete.html"]
        return ["forms/user_delete.html"]


class UserEditHtmxView(TemplateView):
    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["forms/partials/_partial_user_edit.html"]
        return ["forms/user_edit.html"]


class PasswordChangeHtmxView(TemplateView):
    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["forms/partials/_partial_password_change.html"]
        return ["forms/password_change.html"]
