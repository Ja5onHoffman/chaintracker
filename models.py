from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta

class Owner(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bikes = db.relationship('Bike', backref='owner', lazy='dynamic')
    access_token = db.Column(db.String(128))
    refresh_token = db.Column(db.String(128))
    refresh_token_expiration = db.Column(db.DateTime)
    strava_authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Owner {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_refresh_token_expired(self) -> bool:
        return self.refresh_token_expiration < datetime.now()

    def set_refresh_token(self, token, expiration_time):
        self.refresh_token = token
        self.refresh_token_expiration = expiration_time


class Bike(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.String(64), db.ForeignKey('owner.id'))
    parts = db.relationship('Part', backref='bike', lazy='dynamic')
    miles_current = db.Column(db.Float)
    miles_starting = db.Column(db.Float)
    miles_limit = db.Column(db.Float)

    def __repr__(self):
        return '<Bike {}>'.format(self.name)


# Not used yet
class Part(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    part_type = db.Column(Enum('Chain', 'Tire', name='part_type_enum'))
    bike_id = db.Column(db.String(32), db.ForeignKey('bike.id'))
    miles_current = db.Column(db.Float)
    miles_starting = db.Column(db.Float)
    miles_limit = db.Column(db.Float)

    def __repr__(self):
        return '<Part {}>'.format(self.name)

