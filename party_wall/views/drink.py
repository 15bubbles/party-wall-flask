from http import HTTPStatus

from flask import Response, request
from flask_restful import Resource
from party_wall.models.drink import DrinkModel

# TODO: should mimetype be changed to conent_type?
# TODO: I should probably do some marshmallow serialization here


class DrinkListResource(Resource):
    def get(self) -> Response:
        drinks = DrinkModel.objects().to_json()
        return Response(drinks, mimetype="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()
        drink = DrinkModel(**body).save().to_json()
        return Response(drink, mimetype="application/json", status=HTTPStatus.CREATED)


class DrinkDetailsResource(Resource):
    def get(self, id) -> Response:
        drink = DrinkModel.objects.get(id=id).to_json()
        return Response(drink, mimetype="application/json", status=HTTPStatus.OK)

    def put(self, id) -> Response:
        body = request.get_json()
        drink = DrinkModel.objects().get(id=id).update(**body)
        return Response(drink, mimetype="application/json", status=HTTPStatus.OK)

    # def patch(self) -> Response:
    #     pass

    def delete(self, id) -> Response:
        DrinkModel.objects().get(id=id).delete()
        return Response({}, mimetype="application/json", status=HTTPStatus.OK)
