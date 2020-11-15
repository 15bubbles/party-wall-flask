import http
import json
from typing import Union

from flask import Response
from flask_login import LoginManager

from party_wall.authentication.exceptions import RecordNotFound
from party_wall.authentication.hash import BcryptPasswordHasher
from party_wall.authentication.models import UserModel
from party_wall.authentication.repositories import UserAlchemyRepository, UserRepository
from party_wall.authentication.user import User
from party_wall.db import db

# TODO: perhaps this password hasher should be even more separated somehow, because we don't need password hashing
# user creation and no login and logout, neither register
# perhaps I should implement some UseCase for getting user
login_manager = LoginManager()
user_repository = UserAlchemyRepository(UserModel, db.session, BcryptPasswordHasher())


@login_manager.user_loader
def load_user(user_id: str) -> Union[User, None]:
    try:
        user = user_repository.get(user_id)
    except RecordNotFound:
        return None

    return user


@login_manager.unauthorized_handler
def unathorized():
    return Response(
        json.dumps({"error": "Unauthorized"}),
        content_type="application/json",
        status=http.HTTPStatus.UNAUTHORIZED,
    )


# this should be used to use JWT
# @login_manager.request_loader
# def load_request(request):
#     pass
