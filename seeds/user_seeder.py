import bcrypt
from flask_seeder import Seeder

from app.model.user import User


class UserSeeder(Seeder):
    def run(self):
        user = User.query.filter(
            User.email == "admin@admin.com"
        ).first()
        if user:
            return

        user = User()
        user.name = "Admin"
        user.email = "admin@admin.com"
        user.password = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        user.save()
