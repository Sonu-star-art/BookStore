from flask.testing import FlaskClient
from sqlalchemy import JSON
from app import db
from models import User
from flask import Flask, json


def test_register(client: FlaskClient):
    
    data = {'username' : 'mike', 'password' : '12345'}
    response = client.post('/register/submit-register', json=json.dumps(data), headers={'Content-Type' : 'application/json'})
    assert response

    #assert User.query.filter_by(username=data['username']) is not None



