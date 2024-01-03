from flask import request, g
from flask_restful import Resource

from app.resource import auth_required


class ProfileResource(Resource):
    @auth_required
    def get(self):
        user = g.get('user')
        return user.to_dict(), 200
