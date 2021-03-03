from flask import Flask
from todo.config import configurations
from todo.blueprints.landing import landing_bp
from todo.blueprints.users import user_bp
from todo.extensions import db, login_manager, csrf, migrate


def create_app(environment_name="dev"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    app.register_blueprint(landing_bp)
    app.register_blueprint(user_bp)

    return app
