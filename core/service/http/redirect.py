from django.http import HttpResponseRedirect
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from typing import Callable
from django.urls import reverse

from ..alert.alertmessage import AlertMessage


class RedirectWithCtxService:
    alert_manager = AlertMessage

    def __init__(
        self,
        request: Request,
        super_method: Callable,
        success_method: str,
        *args,
        **kwargs,
    ) -> None:
        self.request = request
        self.super_method = super_method
        self.success_method = success_method
        self.args = args
        self.kwargs = kwargs

        self._mngr_instance = self.alert_manager(self.request.session)

    def get_success_ctx(self):
        return getattr(self._mngr_instance, self.success_method)()

    def get_redirect_response(self):
        try:
            self.super_method(self.request, *self.args, **self.kwargs)
            ctx = self.get_success_ctx()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")

        except (KeyError, ValidationError):
            ctx = self._mngr_instance.something_went_wrong()
            return HttpResponseRedirect(f"{reverse('index')}?ctx={ctx}")
