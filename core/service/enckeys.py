from typing import Any, Dict, List, Union

from cryptography.fernet import Fernet


class EncryptionService:
    @staticmethod
    def get_keys(
        session: Dict[str, Any], csrf: Union[str, None] = None
    ) -> Dict[str, str]:
        tokens = {"csrf": csrf} if csrf is not None else {}

        if session.get("encryption_key") is not None:
            tokens["enckey"] = session["encryption_key"]
        else:
            tokens["enckey"] = Fernet.generate_key().decode()

        return tokens

    @staticmethod
    def decrypt_with_key(key: str, *args, **kwargs) -> List[str]:
        fernet = Fernet(key.encode())

        return [fernet.decrypt(arg).decode() for arg in args]
