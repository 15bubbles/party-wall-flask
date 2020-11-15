from abc import ABC, abstractmethod

import bcrypt


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def is_password_valid(self, password: str, hashed_password: str) -> bool:
        pass


class BcryptPasswordHasher(PasswordHasher):
    @staticmethod
    def hash_password(password: str, salt_rounds: int = 12) -> str:
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        return hashed

    @staticmethod
    def is_password_valid(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
