from party_wall.serializing import marshmallow as ma
from party_wall.models.food import FoodModel


class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodModel


class FoodCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodModel
        exclude = ("id",)
