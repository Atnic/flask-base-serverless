import bcrypt
from flask_seeder import Seeder

from app.model.api_key import ApiKey
from app.model.user import User


class ApiKeySeeder(Seeder):
    def run(self):
        user = User.query.filter(
            User.email == "admin@admin.com"
        ).first()
        api_key = ApiKey.query.filter(
            ApiKey.user_id == user.id
        ).first()
        if api_key:
            return

        api_key = ApiKey()
        api_key.user_id = user.id
        api_key.name = "Admin"
        api_key.save()
