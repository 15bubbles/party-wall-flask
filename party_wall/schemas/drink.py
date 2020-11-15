from party_wall.models.drink import DrinkModel
from party_wall.serializing import marshmallow as ma

# TODO: should I create different schema for list and for details and for getting and updates to not have id?


class DrinkSchema(ma.Schema):
    class Meta:
        model = DrinkModel


class DrinkCreateSchema(ma.Schema):
    class Meta:
        model = DrinkModel
        exclude = ("id",)
