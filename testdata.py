from database import db
from app import app  
from models import Owner, Bike, Part 
import logging

def create_test_data():
    logging.info("Creating test data")
    user1 = Owner(username='bob', email='bob@bob.com', password_hash='password', bikes=[])
    user2 = Owner(username='joe', email='joe@joe.com', password_hash='password', bikes=[])
    db.session.add(user1)
    db.session.add(user2)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
    logging.info("Done")
