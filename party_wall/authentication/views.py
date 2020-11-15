import http
import json
from http import HTTPStatus
from typing import Type

from flask import Response, request
from flask_login import current_user, login_required
from flask_login.utils import login_user, logout_user
from flask_restful import Resource
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from party_wall.authentication.exceptions import (
    InvalidCredentials,
    RecordAlreadyExists,
    RecordNotFound,
)
from party_wall.authentication.repositories import UserRepository
from party_wall.authentication.schemas import UserLoginSchema, UserRegisterSchema, UserSchema

# TODO: passing schemas here and relying on their validation error makes it tightly coupled with marshmallow
# perhaps it's possible to raise own exception and to specify it on schema creation?

# TODO: or should I pass initialized Schema instance?
class UsersRegisterResource(Resource):
    def __init__(self, repository: UserRepository, schema_cls: Type[UserRegisterSchema]):
        self.repository = repository
        self.schema_cls = schema_cls

    def post(self) -> Response:
        body = request.get_data(as_text=True)

        try:
            new_user = self.schema_cls().loads(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=http.HTTPStatus.BAD_REQUEST,
            )

        try:
            self.repository.create(new_user)
        except RecordAlreadyExists:
            return Response(
                json.dumps({"error": f"User {new_user.username} already exists"}),
                content_type="application/json",
                status=http.HTTPStatus.BAD_REQUEST,
            )

        return Response(
            json.dumps({"message": f"User {new_user.username} created"}),
            content_type="application/json",
            status=http.HTTPStatus.CREATED,
        )


class UsersLoginResource(Resource):
    def __init__(self, repository: UserRepository, schema_cls: Type[UserLoginSchema]):
        self.repository = repository
        self.schema_cls = schema_cls

    def post(self) -> Response:
        body = request.get_data(as_text=True)

        try:
            data = self.schema_cls().loads(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=http.HTTPStatus.BAD_REQUEST,
            )

        username = data["username"]
        password = data["password"]

        try:
            user = self.repository.login(username, password)
        except InvalidCredentials as err:
            return Response(
                json.dumps({"error": err.message}),
                content_type="application/json",
                status=http.HTTPStatus.BAD_REQUEST,
            )

        login_user(user)
        return Response(
            json.dumps({"message": f"Logged in as {username}"}),
            content_type="application/json",
            status=HTTPStatus.OK,
        )


class UsersLogoutResource(Resource):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @login_required
    def get(self):
        self.repository.logout(current_user)
        logout_user()

        return Response(
            json.dumps({"message": "Logged out"}),
            content_type="application/json",
            status=http.HTTPStatus.OK,
        )


class UsersResource(Resource):
    def __init__(self, repository: UserRepository, schema_cls: Type[UserSchema]):
        self.repository = repository
        self.schema_cls = schema_cls

    @login_required
    def get(self) -> Response:
        users = self.repository.list()

        return Response(
            self.schema_cls().dumps(users, many=True),
            content_type="application/json",
            status=http.HTTPStatus.OK,
        )


class UsersDetailsResource(Resource):
    def __init__(self, repository: UserRepository, schema_cls: Type[UserSchema]):
        self.repository = repository
        self.schema_cls = schema_cls

    @login_required
    def get(self, id: str) -> Response:
        try:
            user = self.repository.get(id)
        except RecordNotFound:
            return Response(
                json.dumps({"error": f"User {id} does not exist"}),
                content_type="application/json",
                status=http.HTTPStatus.NOT_FOUND,
            )

        return Response(
            self.schema_cls().dumps(user),
            content_type="application/json",
            status=http.HTTPStatus.OK,
        )
