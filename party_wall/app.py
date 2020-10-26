from flask import Flask
from flask_restful import Api

from party_wall.settings.base import Config
from party_wall.db import db
from party_wall.serializing import marshmallow
from party_wall.views.food import FoodListResource, FoodDetailsResource
from party_wall.views.drink import DrinkListResource, DrinkDetailsResource

app = Flask(Config.APP_NAME)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)
marshmallow.init_app(app)

api.add_resource(FoodListResource, "/food")
api.add_resource(FoodDetailsResource, "/food/<id>")
api.add_resource(DrinkListResource, "/drinks")
api.add_resource(DrinkDetailsResource, "/drinks/<id>")


if __name__ == "__main__":
    app.run(debug=Config.DEBUG, port=Config.PORT)
