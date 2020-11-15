from typing import Any, Dict

from marshmallow import Schema, fields, post_load, validate

from party_wall.authentication.user import NewUser, User
from party_wall.authentication.validators import (
    MarshmallowPasswordDigitValidator,
    MarshmallowPasswordLowerCaseLetterValidator,
    MarshmallowPasswordSpecialCharacterValidator,
    MarshmallowPasswordUpperCaseLetterValidator,
)

# are some of them qualified to be used with this SQLAlchemy Schema, or does it violate something


class UserRegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(
        load_only=True,
        required=True,
        validate=[
            validate.Length(min=8),
            MarshmallowPasswordDigitValidator(),
            MarshmallowPasswordLowerCaseLetterValidator(),
            MarshmallowPasswordUpperCaseLetterValidator(),
            MarshmallowPasswordSpecialCharacterValidator(),
        ],
    )
    email = fields.Email(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)

    @post_load
    def make_user(self, data: Dict[str, Any], **kwargs) -> NewUser:
        # TODO: not sure if this is a good idea, because it's coupling this schema to this User entity
        # it's a bit coupled either way
        user = NewUser(**data)
        return user


class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)


class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    password = fields.String()
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()


class UserDetailsSchema(Schema):
    username = fields.String()
    password = fields.String()
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()
