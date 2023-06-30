from database import db
from app import app  
from models import Owner, Bike, Part 
import logging

def create_test_data():
    logging.info("Creating test data")
    user1 = Owner(username='bob', email='bob@bob.com', bikes=[])
    user1.set_password('password')
    user2 = Owner(username='joe', email='joe@joe.com', bikes=[])
    user2.set_password('password')
    db.session.add(user1)
    db.session.add(user2)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
    logging.info("Done")

def add_bike():
    logging.info("Adding a bike")
    user = Owner.query.filter_by(username='bob').first()
    bike = Bike(name='bike1', owner_id=user.id, parts=[])
    db.session.add(bike)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
    logging.info("Done")

def add_part():
    logging.info("Adding a part")
    bike = Bike.query.filter_by(name='bike1').first()
    part = Part(name='part1', part_type='type1', bike=bike, miles=0, hours=0, mile_limit=100, hour_limit=100)
    db.session.add(part)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
    logging.info("Done")
