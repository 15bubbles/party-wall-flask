from http import HTTPStatus

from flask import Response, request
from flask_restful import Resource
from party_wall.models.food import FoodModel
from party_wall.schemas.food import FoodSchema

# TODO: some error handling
# TODO: patch updates


class FoodListResource(Resource):
    def get(self) -> Response:
        food = FoodModel.query.all()
        serialized = FoodSchema(many=True).dump(food)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()
        deserialized = FoodSchema().load(body)
        food = FoodModel(**deserialized).save()
        serialized = FoodSchema().dump(food)
        return Response(serialized, content_type="application/json", status=HTTPStatus.CREATED)


class FoodDetailsResource(Resource):
    def get(self, id) -> Response:
        food = FoodModel.query.get(id=id)
        serialized = FoodSchema().dump(food)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def put(self, id) -> Response:
        body = request.get_json()
        deserialized = FoodSchema().load(body)
        food = FoodModel.query.get(id=id).update(**deserialized)
        serialized = FoodSchema().dump(food)
        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def delete(self, id) -> Response:
        FoodModel.query.get(id=id).delete()
        return Response({}, content_type="application/json", status=HTTPStatus.OK)
