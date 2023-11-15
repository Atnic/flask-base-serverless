from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.model import Model

db = SQLAlchemy(model_class=Model)
migrate = Migrate()
