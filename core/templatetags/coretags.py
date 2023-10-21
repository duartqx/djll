from django import template
from django.utils.safestring import mark_safe

from core.service.enckeys import EncryptionService

register = template.Library()

@register.simple_tag(takes_context=True)
def encryption_key(context):

    session = context["request"].session

    encryption_key = EncryptionService.get_keys(session).get("enckey")

    if session.get("encryption_key") is None:
        session["encryption_key"] = encryption_key

    return mark_safe(
        f"""<input type="hidden" name="enckey" value="{encryption_key}"></input>"""
    )
