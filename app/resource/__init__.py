from flask import request, jsonify
from flask_restful import Resource
from flask_sqlalchemy.pagination import Pagination

from app.model import Model


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
        return model, 201


class ModelResource(Resource):
    model = Model

    def get(self, key):
        model = self.model.query.get_or_404(key)
        return model

    def put(self, key):
        model = self.model.query.get_or_404(key)
        data: dict = request.json
        with self.model.query.session.no_autoflush:
            model.set_dict(data)
            model.save()
        return model

    def delete(self, key):
        model = self.model.query.get_or_404(key)
        model.delete()
        return model