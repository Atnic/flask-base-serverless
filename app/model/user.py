from app.db import db


class User(db.Model):
    hidden_fields = ["password"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=db.func.now())
