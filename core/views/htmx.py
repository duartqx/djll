from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            if request.GET:
                return HttpResponseRedirect(
                    reverse("loginform")
                    + "?"
                    + "&".join([f"{key}={value}" for key, value in request.GET.items()])
                )
            return HttpResponseRedirect(reverse("loginform"))
        return super().dispatch(request, *args, **kwargs)


class LoginHtmxView(TemplateView):
    template_name = "forms/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return super().dispatch(request, *args, **kwargs)
