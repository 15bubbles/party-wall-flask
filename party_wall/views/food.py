from http import HTTPStatus

from flask import Response, request
from flask_restful import Resource
from party_wall.models.food import FoodModel

# TODO: should mimetype be changed to conent_type?
# TODO: I should probably do some marshmallow serialization here


class FoodListResource(Resource):
    def get(self) -> Response:
        food = FoodModel.objects().to_json()
        return Response(food, mimetype="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()
        food = FoodModel(**body).save().to_json()
        return Response(food, mimetype="application/json", status=HTTPStatus.CREATED)


class FoodDetailsResource(Resource):
    def get(self, id) -> Response:
        food = FoodModel.objects.get(id=id).to_json()
        return Response(food, mimetype="application/json", status=HTTPStatus.OK)

    def put(self, id) -> Response:
        body = request.get_json()
        food = FoodModel.objects().get(id=id).update(**body)
        return Response(food, mimetype="application/json", status=HTTPStatus.OK)

    # def patch(self) -> Response:
    #     pass

    def delete(self, id) -> Response:
        FoodModel.objects().get(id=id).delete()
        return Response({}, mimetype="application/json", status=HTTPStatus.OK)
