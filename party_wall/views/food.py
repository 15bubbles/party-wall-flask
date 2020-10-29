import json
from http import HTTPStatus

from flask import Response, request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from party_wall.schemas.food import FoodCreateSchema


# TODO: some error handling
# TODO: patch updates


class FoodListResource(Resource):
    def __init__(self, model, schema, logger, db_session):
        self.model = model
        self.schema = schema
        self.logger = logger
        self.db_session = db_session

    def get(self) -> Response:
        food = self.model.query.all()

        serialized = self.schema(many=True).dumps(food)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()

        try:
            deserialized = FoodCreateSchema().load(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=HTTPStatus.BAD_REQUEST,
            )

        food = self.model(**deserialized)
        self.db_session.add(food)
        self.db_session.commit()

        serialized = self.schema().dumps(food)

        return Response(serialized, content_type="application/json", status=HTTPStatus.CREATED)


class FoodDetailsResource(Resource):
    def __init__(self, model, schema, logger, db_session):
        self.model = model
        self.schema = schema
        self.logger = logger
        self.db_session = db_session

    def get(self, id: str) -> Response:
        food = self.model.query.get(id)

        if food is None:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )

        serialized = self.schema().dumps(food)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def put(self, id: str) -> Response:
        body = request.get_json()

        try:
            deserialized = self.schema().load(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=HTTPStatus.BAD_REQUEST,
            )

        updated_count = (
            self.db_session.query(self.model).filter(self.model.id == id).update(deserialized)
        )
        if updated_count == 0:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )
        self.db_session.commit()

        food = self.model.query.get(id)
        serialized = self.schema().dumps(food)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def delete(self, id: str) -> Response:
        deleted_count = self.model.query.filter(self.model.id == id).delete()

        if deleted_count == 0:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )

        self.db_session.commit()

        return Response({}, content_type="application/json", status=HTTPStatus.OK)
