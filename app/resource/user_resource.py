from app.model.user import User
from app.resource import ModelListResource, ModelResource, auth_required


class UserListResource(ModelListResource):
    model = User

    @auth_required
    def get(self):
        return super(UserListResource, self).get()

    @auth_required
    def post(self):
        return super(UserListResource, self).post()


class UserResource(ModelResource):
    model = User

    @auth_required
    def get(self, key):
        return super(UserResource, self).get(key)

    @auth_required
    def put(self, key):
        return super(UserResource, self).put(key)

    @auth_required
    def delete(self, key):
        return super(UserResource, self).delete(key)
