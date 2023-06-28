from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Owner
from database import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# A route that reads something from the database to test the database
@app.route('/read')
def read():
    users = Owner.query.all()  # fetches all User records
    for user in users:
        print("username:", user.username)
        print("password:", user.password_hash)
        print("email:", user.email)
        print("id:", user.id)
    return "Read successful"


if __name__ == "__main__":
    app.run(debug=True)
