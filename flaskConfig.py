import os

class config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "FLASK_SECRET_KEY environment variable is not set. "
            "Set it before starting the application."
        )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///database.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


