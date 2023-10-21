from django import template
from django.utils.safestring import mark_safe

from core.service.enckeys import EncryptionService

register = template.Library()


def get_key(session) -> str:
    encryption_key = EncryptionService.get_keys(session).get("enckey", "")

    if session.get("encryption_key") is None:
        session["encryption_key"] = encryption_key

    return encryption_key


@register.simple_tag(takes_context=True)
def encryption_key(context):
    enckey = get_key(context["request"].session)
    return mark_safe(
        f"""<input type="hidden" name="enckey" value="{enckey}"></input>"""
    )


@register.simple_tag(takes_context=True)
def get_encryption_key(context):
    return get_key(context["request"].session)
