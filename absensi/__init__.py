import os

from flask import Flask,jsonify
from . import api,services
from sqlalchemy import create_engine

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config['engine']=create_engine(os.path.join('sqlite:///', 'flaskr.sqlite'), echo=True, future=True)

    app.register_blueprint(api.bp)
    app.register_blueprint(services.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    

    return app