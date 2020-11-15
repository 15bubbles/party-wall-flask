import json
from http import HTTPStatus

from flask import Response, request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from party_wall.models.drink import DrinkModel
from party_wall.schemas.drink import DrinkCreateSchema, DrinkSchema

# TODO: some error handling
# TODO: patch update


class DrinkListResource(Resource):
    def __init__(self, model, schema, logger, db_session):
        self.model = model
        self.schema = schema
        self.logger = logger
        self.db_session = db_session

    def get(self) -> Response:
        drinks = self.model.query.all()

        serialized = self.schema(many=True).dumps(drinks)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def post(self) -> Response:
        body = request.get_json()

        try:
            deserialized = DrinkCreateSchema().load(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=HTTPStatus.BAD_REQUEST,
            )

        drink = self.model(**deserialized)
        self.db_session.add(drink)
        self.db_session.commit()

        serialized = DrinkSchema().dumps(drink)

        return Response(serialized, content_type="application/json", status=HTTPStatus.CREATED)


class DrinkDetailsResource(Resource):
    def __init__(self, model, schema, logger, db_session):
        self.model = model
        self.schema = schema
        self.logger = logger
        self.db_session = db_session

    def get(self, id) -> Response:
        drink = self.model.query.get(id)

        if drink is None:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )

        serialized = self.schema().dumps(drink)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def put(self, id) -> Response:
        body = request.get_json()

        try:
            deserialized = DrinkSchema().load(body)
        except ValidationError as err:
            return Response(
                json.dumps(err.messages),
                content_type="application/json",
                status=HTTPStatus.BAD_REQUEST,
            )

        updated_count = self.model.query.filter(self.model.id == id).update(deserialized)
        if updated_count == 0:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )
        self.db_session.commit()

        drink = self.model.query.get(id)
        serialized = self.schema().dumps(drink)

        return Response(serialized, content_type="application/json", status=HTTPStatus.OK)

    def delete(self, id) -> Response:
        deleted_count = self.model.query.filter(self.model.id == id).delete()

        if deleted_count == 0:
            return Response(
                json.dumps({"error": "Not found"}),
                content_type="application/json",
                status=HTTPStatus.NOT_FOUND,
            )

        self.db_session.commit()

        return Response({}, content_type="application/json", status=HTTPStatus.OK)
