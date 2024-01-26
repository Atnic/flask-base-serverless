import datetime

from flask_sqlalchemy.model import Model as BaseModel
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError


class Model(BaseModel):
    hidden_fields = []

    @classmethod
    def get_pks(cls):
        return tuple(key.name for key in inspect(cls).primary_key)

    @classmethod
    def get_pk(cls):
        try:
            return cls.get_pks()[0]
        except IndexError:
            return None

    def get_pk_values(self):
        return inspect(self).identity

    def get_pk_value(self):
        return self.get_pk_values()[0]

    def save(self):
        try:
            if self.get_pk_values() is None:
                if hasattr(self, 'created_at'):
                    self.created_at = datetime.datetime.utcnow()
                self.query.session.add(self)
            if hasattr(self, 'updated_at'):
                self.updated_at = datetime.datetime.utcnow()
            self.query.session.commit()
        except OperationalError as e:
            self.query.session.rollback()
            raise e

    def delete(self):
        try:
            self.query.session.delete(self)
            self.query.session.commit()
        except OperationalError as e:
            self.query.session.rollback()
            raise e

    def to_dict(self):
        data: dict = {}
        columns = self.__dict__.keys()
        for column in columns:
            if column.startswith('_'):
                continue
            if column in self.hidden_fields:
                continue
            c = getattr(self, column)
            if isinstance(c, datetime.datetime):
                c = c.isoformat()
            data[column] = c
        return data

    def set_dict(self, data: dict):
        columns = self.__table__.columns
        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

        return self
