from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Tempusers(UserMixin, db.Model):

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), unique = True, nullable=False)
        username = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(), nullable=False)
        verified = db.Column(db.Boolean(), default=False)

class Users(UserMixin, db.Model):

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), unique = True, nullable=False)
        username = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(), nullable=False)
        