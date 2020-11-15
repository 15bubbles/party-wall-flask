from flask_restful import Api

from party_wall.authentication.hash import BcryptPasswordHasher
from party_wall.authentication.models import UserModel
from party_wall.authentication.repositories import UserAlchemyRepository
from party_wall.authentication.schemas import UserLoginSchema, UserRegisterSchema, UserSchema
from party_wall.authentication.views import (
    UsersDetailsResource,
    UsersLoginResource,
    UsersLogoutResource,
    UsersRegisterResource,
    UsersResource,
)
from party_wall.db import db
from party_wall.logging import logger
from party_wall.models.drink import DrinkModel
from party_wall.models.food import FoodModel
from party_wall.schemas.drink import DrinkSchema
from party_wall.schemas.food import FoodSchema
from party_wall.views.drink import DrinkDetailsResource, DrinkListResource
from party_wall.views.food import FoodDetailsResource, FoodListResource

api = Api()
common_kwargs = {"logger": logger, "db_session": db.session}

# AUTHENTICATION
user_repository = UserAlchemyRepository(
    model=UserModel, session=db.session, password_hasher=BcryptPasswordHasher()
)

api.add_resource(
    UsersRegisterResource,
    "/register",
    resource_class_kwargs={"repository": user_repository, "schema_cls": UserRegisterSchema},
)
api.add_resource(
    UsersLoginResource,
    "/login",
    resource_class_kwargs={"repository": user_repository, "schema_cls": UserLoginSchema},
)
api.add_resource(
    UsersLogoutResource, "/logout", resource_class_kwargs={"repository": user_repository}
)
api.add_resource(
    UsersResource,
    "/users",
    resource_class_kwargs={"repository": user_repository, "schema_cls": UserSchema},
)
api.add_resource(
    UsersDetailsResource,
    "/users/<string:id>",
    resource_class_kwargs={"repository": user_repository, "schema_cls": UserSchema},
)


# FOOD / DRINKS

api.add_resource(
    FoodListResource,
    "/food",
    resource_class_kwargs={
        **common_kwargs,
        "model": FoodModel,
        "schema": FoodSchema,
    },
)
api.add_resource(
    FoodDetailsResource,
    "/food/<string:id>",
    resource_class_kwargs={
        **common_kwargs,
        "model": FoodModel,
        "schema": FoodSchema,
    },
)
api.add_resource(
    DrinkListResource,
    "/drinks",
    resource_class_kwargs={
        **common_kwargs,
        "model": DrinkModel,
        "schema": DrinkSchema,
    },
)
api.add_resource(
    DrinkDetailsResource,
    "/drinks/<string:id>",
    resource_class_kwargs={
        **common_kwargs,
        "model": DrinkModel,
        "schema": DrinkSchema,
    },
)
