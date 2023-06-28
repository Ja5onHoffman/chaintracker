from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Owner(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bikes = db.relationship('Bike', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<Owner {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    parts = db.relationship('Part', backref='bike', lazy='dynamic')

    def __repr__(self):
        return '<Bike {}>'.format(self.name)


class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    part_type = db.Column(Enum('type1', 'type2', name='part_type_enum'))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'))
    miles = db.Column(db.Integer)
    hours = db.Column(db.Integer)
    mile_limit = db.Column(db.Integer)
    hour_limit = db.Column(db.Integer)

    def __repr__(self):
        return '<Part {}>'.format(self.name)

