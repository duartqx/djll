from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from core.views.auth import LoginView

from ..views.user import CreateUserView


class GetMixin:
    template_name = ""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, self.template_name)


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.GET:
                return HttpResponseRedirect(
                    reverse("loginform")
                    + "?"
                    + "&".join(
                        [
                            f"{key}={value}"
                            for key, value in request.GET.items()
                        ]
                    )
                )
            return HttpResponseRedirect(reverse("loginform"))
        return super().dispatch(request, *args, **kwargs)


class LoginHtmxView(GetMixin, LoginView):
    template_name = "forms/login.html"

    @method_decorator(csrf_protect)
    def login(self, *args, **kwargs):
        if self.get_serializer().login():
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(f"{reverse('loginform')}?somethingwrong=1")


class CreateUserHtmxView(GetMixin, CreateUserView):
    template_name = "forms/user_create.html"

    @method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            return HttpResponseRedirect(
                f"{reverse('index')}?account_creation=1"
            )
        except KeyError:
            return HttpResponseRedirect(f"{reverse('index')}?somethingwrong=1")
