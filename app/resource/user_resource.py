from app.model.user import User
from app.resource import ModelListResource, ModelResource


class UserListResource(ModelListResource):
    model = User

    def get(self):
        return super(UserListResource, self).get()

    def post(self):
        return super(UserListResource, self).post()


class UserResource(ModelResource):
    model = User

    def get(self, key):
        return super(UserResource, self).get(key)

    def put(self, key):
        return super(UserResource, self).put(key)

    def delete(self, key):
        return super(UserResource, self).delete(key)
