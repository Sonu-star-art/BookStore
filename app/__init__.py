from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app=app)

    # Import blueprints
    from app.authentication import auth
    from app.main import main
    from app.admin import admin

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    # Create database
    with app.app_context():
        db.create_all()

    return app








