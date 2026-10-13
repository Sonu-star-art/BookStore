from flask import Flask
import pytest
from app import create_app


class testConfig:
    SECRET_KEY = "testkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In memory for storing test databases
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


@pytest.fixture
def app():
    app = create_app(testConfig)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_app_creation():
    assert app is not None