from flask import request
from flask_restful import Resource


class LoginResource(Resource):
    def post(self):
        data: dict = request.json
        if not data.get("username"):
            return {"message": "Username is required"}, 400
        if not data.get("password"):
            return {"message": "Password is required"}, 400
        from app.model.user import User
        user = User.query.filter_by(email=data["username"]).first()
        if not user:
            return {"message": "Invalid username or password"}, 400
        if not user.check_password(data["password"]):
            return {"message": "Invalid username or password"}, 400
        from app.model.api_key import ApiKey
        api_key = ApiKey.query.filter_by(user_id=user.id).first()
        if not api_key:
            api_key = ApiKey(user_id=user.id)
            api_key.save()
        return {"api_key": api_key.id}, 200
