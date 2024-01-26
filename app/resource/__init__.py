import functools

from flask import request, jsonify, g
from flask_restful import Resource
from flask_sqlalchemy.pagination import Pagination

from app.model import Model


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in g and g.user:
            return func(*args, **kwargs)
        api_key = request.headers.get("X-Api-Key", request.args.get('api_key', None))
        if not api_key:
            return {"message": "API key is required"}, 401
        from app.model.api_key import ApiKey
        api_key = ApiKey.query.get(api_key)
        if not api_key:
            return {"message": "Invalid API key"}, 401
        g.user = api_key.user
        return func(*args, **kwargs)

    try:
        return wrapper
    except RuntimeError:
        return func


class ModelListResource(Resource):
    model = Model

    def get(self):
        models: Pagination = self.model.query.paginate(
            page=int(request.args.get("page", 1)),
            per_page=int(request.args.get("per_page", 15)),
            error_out=False,
            max_per_page=1000
        )

        return jsonify({
            "data": [model.to_dict() for model in models.items],
            "meta": {
                "page": models.page,
                "per_page": models.per_page,
                "total": models.total
            }
        })

    def post(self):
        data: dict = request.json
        with self.model.query.session.no_autoflush:
            model = self.model()
            model.set_dict(data)
            model.save()
        return model.to_dict(), 201


class ModelResource(Resource):
    model = Model

    def get(self, key):
        model = self.model.query.get_or_404(key)
        return model.to_dict()

    def put(self, key):
        model = self.model.query.get_or_404(key)
        data: dict = request.json
        with self.model.query.session.no_autoflush:
            model.set_dict(data)
            model.save()
        return model.to_dict()

    def delete(self, key):
        model = self.model.query.get_or_404(key)
        model.delete()
        return model.to_dict()
