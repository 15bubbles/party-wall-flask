from flask_restful import Api

from party_wall.db import db

from party_wall.logging import logger
from party_wall.models.drink import DrinkModel
from party_wall.models.food import FoodModel
from party_wall.schemas.drink import DrinkSchema
from party_wall.schemas.food import FoodSchema
from party_wall.views.drink import DrinkDetailsResource, DrinkListResource
from party_wall.views.food import FoodDetailsResource, FoodListResource

common_kwargs = {"logger": logger, "db_session": db.session}

api = Api()
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
