from flask import Flask
from app import create_app
from flaskConfig import config

app = create_app(config)

if __name__ == "__main__":
    app.run(debug=True)


  