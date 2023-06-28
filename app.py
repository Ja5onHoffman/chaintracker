from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Owner
from database import db
import os
from dotenv import load_dotenv
from forms import LoginForm, RegistrationForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#LoginManager
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return Owner.query.get(int(id))

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If the user is already logged in, redirect to the index page
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Owner.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            # If the username or password is invalid, redirect to the login page
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


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
