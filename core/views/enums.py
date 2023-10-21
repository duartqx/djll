from enum import StrEnum

class AlertMessage(StrEnum):
    SOMETHING_WENT_WRONG = "Something Went Wrong"
    ACCOUNT_SUCCESSFULLY_CREATED = "Your account was sucessfully created!"

class AlertBootstrapClass(StrEnum):
    SUCCESS = "alert-success"
    DANGER = "alert-danger"
