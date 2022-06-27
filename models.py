import os
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from flask_sqlalchemy import SQLAlchemy
import json, sys

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	db.create_all()

#--------------------- Models-------------------------#

class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(db.String, unique=True, nullable=False)
    release_date = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, title, release_date=datetime.now()):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f"< Movie {self.id} {self.title}>"
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(120), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(40), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"< Actor {self.id} {self.name}>"
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
