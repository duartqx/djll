from enum import StrEnum
from typing import Any, Dict

from ..encryption.fernet import FernetEncryptionService


class AlertMessageStatus(StrEnum):
    SOMETHING_WENT_WRONG = "Something Went Wrong"
    ACCOUNT_SUCCESSFULLY_CREATED = "Your account was sucessfully created!"
    SUCCESSFULLY_CHANGED_PASSWORD = "Your password was successfully updated!"
    SUCCESSFULLY_UPDATED_USER = "Your informations were successfully updated!"
    SUCCESSFULLY_DELETED_USER = "Your account was successfully deleted!"
    YOU_WERE_LOGGED_OUT = "You were logged out"
    NOT_AUTHENTICATED = "You are not authenticated!"


class AlertBootstrapClass(StrEnum):
    SUCCESS = "alert-success"
    DANGER = "alert-danger"
    WARNING = "alert-warning"
    INFO = "alert-info"


class AlertMessage:
    provider = FernetEncryptionService

    def __init__(self, session: Dict[str, Any]) -> None:
        self.session = session
        self.service = self.provider(self.session)

    def successfully_created_account(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.ACCOUNT_SUCCESSFULLY_CREATED,
                "alertclass": AlertBootstrapClass.SUCCESS,
            }
        )

    def successfully_updated_user(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.SUCCESSFULLY_UPDATED_USER,
                "alertclass": AlertBootstrapClass.SUCCESS,
            }
        )

    def successfully_deleted_user(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.SUCCESSFULLY_DELETED_USER,
                "alertclass": AlertBootstrapClass.WARNING,
            }
        )

    def you_are_not_authenticated(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.NOT_AUTHENTICATED,
                "alertclass": AlertBootstrapClass.WARNING,
            }
        )

    def logout(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.YOU_WERE_LOGGED_OUT,
                "alertclass": AlertBootstrapClass.INFO,
            }
        )

    def successfully_changed_password(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.SUCCESSFULLY_CHANGED_PASSWORD,
                "alertclass": AlertBootstrapClass.SUCCESS,
            }
        )

    def something_went_wrong(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.SOMETHING_WENT_WRONG,
                "alertclass": AlertBootstrapClass.DANGER,
            }
        )

    def decrypt_ctx(self, ctx: str) -> Dict[str, str]:
        return self.service.decrypt_ctx(ctx)
