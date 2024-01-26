import os

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd() + '/instance', 'app.sqlite')}"
SQLALCHEMY_BINDS = {
    "metabase": {
        "url": f"mysql+pymysql://username:password@localhost:3306/metabase"
    },
    "jala": {
        "url": "mysql+pymysql://username:password@localhost:3306/jala-web",
    },
}
