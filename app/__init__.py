import os
import traceback

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import HTTPException


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'app.sqlite')}"
    )

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

    from .db import db, migrate, seeder
    db.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)

    CORS(app)
    api = Api(app)

    from app.resource.auth_resource import LoginResource
    from app.resource.profile_resource import ProfileResource
    from app.resource.user_resource import UserListResource, UserResource
    from app.resource.api_key_resource import ApiKeyListResource, ApiKeyResource

    api.add_resource(LoginResource, '/login')
    api.add_resource(ProfileResource, '/profile')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:key>')
    api.add_resource(ApiKeyListResource, '/api_keys')
    api.add_resource(ApiKeyResource, '/api_keys/<string:key>')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.errorhandler(404)
    def resource_not_found(e):
        return make_response(jsonify(error='Not found!'), 404)

    @app.errorhandler(Exception)
    def handle_error(e):
        traceback.print_exc()
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    return app
