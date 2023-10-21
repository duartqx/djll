from enum import StrEnum
from typing import Any, Dict

from ..service.encryption import EncryptionService


class AlertMessageStatus(StrEnum):
    SOMETHING_WENT_WRONG = "Something Went Wrong"
    ACCOUNT_SUCCESSFULLY_CREATED = "Your account was sucessfully created!"


class AlertBootstrapClass(StrEnum):
    SUCCESS = "alert-success"
    DANGER = "alert-danger"


class AlertMessage:
    def __init__(self, session: Dict[str, Any]) -> None:
        self.session = session
        self.service = EncryptionService(self.session)

    def successfully_created_account(self) -> str:
        return self.service.encrypt_json(
            {
                "alertmessage": AlertMessageStatus.ACCOUNT_SUCCESSFULLY_CREATED,
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
