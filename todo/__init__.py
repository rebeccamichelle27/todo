from flask import Flask
from todo.config import configurations
from todo.blueprints.landing import landing_bp
from todo.extensions import db


def create_app(environment_name="dev"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)

    app.register_blueprint(landing_bp)

    return app
