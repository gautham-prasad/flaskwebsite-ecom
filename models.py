from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class tempusers(db.Model):

        __tablename__ = "tempusers"

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), unique = True, nullable=False)
        username = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(), nullable=False)

class users(UserMixin, db.Model):

        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), unique = True, nullable=False)
        username = db.Column(db.String(100), unique=True, nullable=False)

class usersinfo(UserMixin, db.Model):

        __tablename__ = "usersinfo"

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), unique = True, nullable=False)
        password = db.Column(db.String(), nullable=False)

