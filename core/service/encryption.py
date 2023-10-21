import json

from typing import Any, Dict, List, TypeAlias, Union
from cryptography.fernet import Fernet

Serializable: TypeAlias = Dict[str, Union[int, str, List[Union[int, str]]]]


class NotSerializableError(TypeError):
    pass


class MissingEncryptionKey(Exception):
    pass


class EncryptionService:
    provider = Fernet

    def __init__(
        self,
        session: Union[Dict[str, Any], None] = None,
        csrf: Union[str, None] = None,
        raise_exception: bool = False,
    ) -> None:
        if session is None:
            session = {}

        self.raise_exception = raise_exception
        self.session = session
        self.csrf = csrf
        self.fernet = self.provider(self.get_enckey().encode())

    def generate_key(self) -> str:
        return self.provider.generate_key().decode()

    def get_enckey(self) -> str:
        if self.session.get("encryption_key") is not None:
            return self.session["encryption_key"]

        if self.raise_exception:
            raise MissingEncryptionKey()

        self.session["encryption_key"] = self.generate_key()
        return self.session["encryption_key"]

    def get_tokens(self) -> Dict[str, str]:
        encryption_key = self.get_enckey()
        if self.csrf is not None:
            return {"csrf": self.csrf, "enckey": encryption_key}
        return {"enckey": encryption_key}

    def decrypt_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("enc"):
            return data
        unencrypted_data = {}
        for field, value in filter(lambda d: d[0] != "enc", data.items()):
            unencrypted_data[field] = self.fernet.decrypt(value).decode()
        return unencrypted_data

    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data).decode()

    def decrypt_ctx(self, data: str) -> Dict[str, str]:
        return json.loads(self.decrypt(data))

    def decrypt_list(self, *args, **kwargs) -> List[str]:
        return [self.fernet.decrypt(arg).decode() for arg in args]

    def encrypt_json(self, se: Serializable, *args, **kwargs) -> str:
        """
        @Raises: NotSerializableError
        """
        try:
            serialized: str = json.dumps(se)
        except TypeError as e:
            raise NotSerializableError(e)
        return self.fernet.encrypt(serialized.encode()).decode()
