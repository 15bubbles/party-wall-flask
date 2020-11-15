import sys
from abc import ABC, abstractmethod
from typing import Any, List

from party_wall.authentication.exceptions import (
    InvalidCredentials,
    RecordAlreadyExists,
    RecordNotFound,
)
from party_wall.authentication.hash import PasswordHasher
from party_wall.authentication.user import NewUser, User


class UserRepository(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def logout(self, user: User):
        # should we pass whole instance here or just id
        pass

    @abstractmethod
    def create(self, new_user: NewUser):
        # perhaps it should return some count of created items?
        pass

    @abstractmethod
    def get(self, id: Any) -> User:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User):
        pass

    @abstractmethod
    def delete(self, id: Any):
        # perhaps it should return number of deleted items?
        pass


class UserAlchemyRepository(UserRepository):
    def __init__(self, model, session, password_hasher: PasswordHasher):
        self.model = model
        self.session = session
        self.password_hasher = password_hasher

    def _hash_password(self, password: str) -> str:
        return self.password_hasher.hash_password(password)

    def _is_password_valid(self, password: str, hashed_password: str) -> bool:
        return self.password_hasher.is_password_valid(password, hashed_password)

    def _build_user(self, user) -> User:
        return User(
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.authenticated,
            user.superuser,
        )

    def login(self, username: str, password: str):
        user = self.model.query.filter_by(username=username).first()

        if user is None or not self._is_password_valid(password, user.password):
            raise InvalidCredentials("Invalid credentials provided")

        user.authenticated = True
        self.session.commit()

        return self._build_user(user)

    def logout(self, user: User):
        existing_user = self.model.query.filter_by(id=user.id).first()

        if existing_user is None:
            raise RecordNotFound(f"User with id '{user.id}' does not exist")

        existing_user.authenticated = False
        self.session.commit()

    def create(self, new_user: NewUser):
        existing_user = self.model.query.filter_by(username=new_user.username)

        if existing_user is None:
            raise RecordAlreadyExists(f"User with '{new_user.username}' already exists")

        new_user.password = self._hash_password(new_user.password)
        new_user = self.model(**new_user.to_dict())
        self.session.add(new_user)
        self.session.commit()

    def get(self, id: str, **kwargs) -> User:
        user = self.model.query.filter_by(id=id).first()

        if user is None:
            raise RecordNotFound(f"User with id '{id}' does not exist")

        return self._build_user(user)

    def list(self) -> List[User]:
        users = self.model.query.all()

        return [self._build_user(user) for user in users]

    def update(self, user: User):
        pass

    def delete(self, id: str):
        user = self.model.query.filter_by(id=id).first()

        if user is None:
            raise RecordNotFound(f"User with id '{id}' does not exist")

        self.session.remove(user)
        self.session.commit()
