from django import template
from django.utils.safestring import mark_safe

from ..service.encryption.fernet import FernetEncryptionService

register = template.Library()


class EncryptionKeyTag:
    service = FernetEncryptionService

    @classmethod
    def get_key(cls, session) -> str:
        encryption_key = cls.service(session).get_enckey()

        if session.get("encryption_key") is None:
            session["encryption_key"] = encryption_key

        return encryption_key

    @classmethod
    def encryption_key_wrapper(cls):
        @register.simple_tag(takes_context=True)
        def encryption_key(context):
            enckey = cls.get_key(context["request"].session)
            return mark_safe(
                f"""<input type="hidden" name="enckey" value="{enckey}"></input>"""
            )

        return encryption_key

    @classmethod
    def get_encryption_key_wrapper(cls):
        @register.simple_tag(takes_context=True)
        def get_encryption_key(context):
            return cls.get_key(context["request"].session)

        return get_encryption_key

    @classmethod
    def build(cls):
        cls.get_encryption_key_wrapper()
        cls.encryption_key_wrapper()


EncryptionKeyTag.build()
