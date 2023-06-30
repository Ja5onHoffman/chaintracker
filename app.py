from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Owner, Bike, Part
from database import db
import os
from dotenv import load_dotenv
from forms import LoginForm, RegistrationForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Owner.query.get(int(user_id))

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userhome', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = Owner.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('userhome', username=user.username))
        else:
            flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/user/<username>')
@login_required
def userhome(username):
    user = Owner.query.filter_by(username=username).first_or_404()
    bikes = user.bikes.all()
    return render_template('userhome.html', user=user, bikes=bikes)

@app.route('/bike/<int:bike_id>')
@login_required
def bike(user):
    return render_template('bike.html', bike=bike.id)

@app.route('/read')
def read():
    owners = Owner.query.all()
    for owner in owners:
        print("username:", owner.username)
        print("email:", owner.email)
        print("id:", owner.id)
    return "Read successful"

if __name__ == "__main__":
    app.run(debug=True)
