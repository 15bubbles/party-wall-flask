import os

from flask import Flask
from flask_migrate import Migrate

from party_wall.api import api
from party_wall.auth import login_manager
from party_wall.db import db
from party_wall.serializing import marshmallow
from party_wall.settings.base import Config

app = Flask(Config.APP_NAME)
app.config.from_object(Config)
api.init_app(app)
db.init_app(app)
marshmallow.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.debug = True
    app.run(debug=Config.DEBUG, port=Config.PORT)
