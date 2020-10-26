from http import HTTPStatus
from os import set_inheritable

from flask import Response, request
from flask_restful import Resource
from party_wall.models.drink import DrinkModel
from party_wall.schemas.drink import DrinkSchema

# TODO: some error handling
# TODO: patch update


class DrinkListResource(Resource):
    def get(self) -> Response:
        drinks = Drink.query.all()
        serialized = DrinkSchema(many=True).dump(drinks)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()
        deserialized = DrinkSchema().load(body)
        drink = DrinkModel(**deserialized).save()
        serialized = DrinkSchema().dump(drink)
        return Response(serialized, content_type="application/json", status=HTTPStatus.CREATED)


class DrinkDetailsResource(Resource):
    def get(self, id) -> Response:
        drink = Drink.query.get(id=id)
        serialized = DrinkSchema().dump(drink)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def put(self, id) -> Response:
        body = request.get_json()
        deserialized = DrinkSchema().load(body)
        drink = DrinkModel.get(id=id).update(**deserialized)
        serialized = Drinkschema().dump(drink)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def delete(self, id) -> Response:
        DrinkModel.query.get(id=id).delete()
        return Response({}, content_type="application/json", status=HTTPStatus.OK)
