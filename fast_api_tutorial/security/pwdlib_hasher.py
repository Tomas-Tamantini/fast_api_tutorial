from pwdlib import PasswordHash


class PwdLibHasher:
    def __init__(self):
        self._pwd_context = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
