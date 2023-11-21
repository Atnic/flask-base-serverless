from flask_restful import abort

from app.model.api_key import ApiKey
from app.resource import ModelListResource, ModelResource, auth_required


class ApiKeyListResource(ModelListResource):
    model = ApiKey

    def get(self):
        abort(404)
        return super(ApiKeyListResource, self).get()

    @auth_required
    def post(self):
        return super(ApiKeyListResource, self).post()


class ApiKeyResource(ModelResource):
    model = ApiKey

    def get(self, key):
        abort(404)
        return super(ApiKeyResource, self).get(key)

    def put(self, key):
        abort(404)
        return super(ApiKeyResource, self).put(key)

    @auth_required
    def delete(self, key):
        return super(ApiKeyResource, self).delete(key)
