from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="./client/dist")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://yura@/slowdash"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = SQLAlchemy(app)


import slowdash.server.api
import slowdash.server.models
import slowdash.server.routes
