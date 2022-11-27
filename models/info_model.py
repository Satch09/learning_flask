from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InfoModel(db.Model):
    __tablename__ = 'info_table'

    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    eye_colour = db.Column(db.String())

    def __init__(self, name, age, eye_colour):
        self.name = name
        self.age = age
        self.eye_colour = eye_colour

    def __repr__(self):
        return f"{self.name}:{self.age}, {self.eye_colour}"
