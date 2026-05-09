import os
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self, key_path="jarvis_key.key"):
        self.key_path = key_path
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt(self, data: str) -> bytes:
        if not data:
            return b""
        return self.fernet.encrypt(data.encode())

    def decrypt(self, token: bytes) -> str:
        if not token:
            return ""
        return self.fernet.decrypt(token).decode()
