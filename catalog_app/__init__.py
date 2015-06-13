from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_app.api.models import Base

from settings import config


engine = create_engine(
    config.DATABASE_URI
)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


from catalog_app.api.auth import auth
from catalog_app.api.controllers import api, root


app = Flask(__name__)
app.register_blueprint(root)
app.register_blueprint(api)
app.register_blueprint(auth)
