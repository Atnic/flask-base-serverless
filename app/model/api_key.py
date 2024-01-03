import secrets

from app.db import db


class ApiKey(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=db.func.now())

    user = db.relationship('User', backref=db.backref('api_keys', lazy=True))

    def save(self):
        if self.id is None:
            self.id = secrets.token_hex(16)
        return super(ApiKey, self).save()
