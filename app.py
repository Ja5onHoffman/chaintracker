from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Owner, Bike, Part
from database import db
import os
from dotenv import load_dotenv
from forms import LoginForm, RegistrationForm, PartForm, BikeForm
from flask_migrate import Migrate
from stravalib.client import Client 
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

migrate = Migrate(app, db)

# stravalib Client
client = Client()

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
    # logout_user()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # logout_user() # logout for now to test login
        user = Owner.query.filter_by(username=current_user.username).first()
        if user.strava_authenticated:
            client.access_token = user.access_token

            if user.refresh_token_expiration > datetime.now():
                refresh_response = client.refresh_access_token(client_id=os.getenv('CLIENT_ID'), 
                                                                client_secret=os.getenv('CLIENT_SECRET'), 
                                                                refresh_token=user.refresh_token)
                user.access_token = refresh_response['access_token']
                user.refresh_token = refresh_response['refresh_token']
                user.refresh_token_expiration = datetime.fromtimestamp(refresh_response['expires_at'])
                db.session.commit()

        return redirect(url_for('userhome', username=current_user.username))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Owner.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['strava_authenticated'] = user.strava_authenticated
            if not user.strava_authenticated:
                session['auth_complete'] = False
            return redirect(url_for('userhome', username=user.username))
        else:
            flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/bikes')
@login_required
def bikes():
    bikes = client.get_gear()
    print(bikes)
    return redirect(url_for('userhome', username=current_user.username))

@app.route('/add_bike', methods=['GET', 'POST'])
@login_required
def add_bike():
    athlete = client.get_athlete()
    bikes = athlete.bikes

    form = BikeForm()
    form.bikes.choices = [(bike.id, bike.name) for bike in bikes]

    if form.validate_on_submit():
        selected_bike_ids = form.bikes.data
        owner_id = current_user.id
        
        selected_bikes = [bike for bike in bikes if bike.id in selected_bike_ids]

        for bike in selected_bikes:
            bike = Bike(id = bike.id,
                        name = bike.name,
                        owner_id = owner_id,
                        miles = bike.distance)
            db.session.add(bike)
            db.session.commit()
        return redirect(url_for('userhome', username=current_user.username))

    return render_template('add_bike.html', form=form)


@app.route('/stravacallback')
@login_required
def strava_callback():
    username = current_user.username

    code = request.args.get('code')
    token_response = client.exchange_code_for_token(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'), code=code)
    user = Owner.query.filter_by(username=username).first_or_404()
    user.access_token = token_response['access_token']
    client.access_token = token_response['access_token']
    user.refresh_token = token_response['refresh_token']
    user.refresh_token_expiration = datetime.fromtimestamp(token_response['expires_at'])
    user.strava_authenticated = True
    db.session.commit()

    return redirect(url_for('userhome', username=current_user.username))

    
@app.route('/user/<username>')
@login_required
def userhome(username):
    strava_authenticated = session.get('strava_authenticated', False)
    url = None
    if not strava_authenticated:
        url = client.authorization_url(client_id=os.getenv('CLIENT_ID'), 
                                redirect_uri=f'http://127.0.0.1:5000/stravacallback',
                                scope='read_all',
                                approval_prompt='auto')
        # Add unsupported scopes
        scopes = 'activity:read_all,profile:read_all'

        # Find the index of 'scope=' in the URL
        index_start = url.index('scope=')
        index_end = url.index('&', index_start)

        # Replace the scope with the desired scopes
        new_url = url[:index_start] + 'scope=' + scopes + url[index_end:]
        url = new_url
        print(url)
    user = Owner.query.filter_by(username=username).first_or_404()
    bikes = user.bikes.all()
    return render_template('userhome.html', user=user, bikes=bikes, authorize_url=url)

@app.route('/bike/<int:bike_id>')
@login_required
def bike(bike_id):
    form = PartForm()
    bike = Bike.query.get(bike_id)
    return render_template('bike.html', bike=bike, bike_id=bike_id, form=form)

@app.route('/part/<int:part_id>')
@login_required
def part(part_id):
    part = Part.query.get(part_id)
    return render_template('part.html', part=part)

@app.route('/add_part/<int:bike_id>', methods=['GET', 'POST'])
@login_required
def add_part(bike_id):
    bike = Bike.query.get(bike_id)
    form = PartForm()
    if form.validate_on_submit():
        part = Part(name=form.name.data, 
                    part_type=form.part_type.data, 
                    bike_id=bike.id, 
                    miles=form.miles.data, #These will need to pull current miles from strava
                    hours=form.hours.data, 
                    mile_limit=form.mile_limit.data, 
                    hour_limit=form.hour_limit.data)
        db.session.add(part)
        db.session.commit()
        flash("Congratulations, you added a part!")
        return redirect(url_for('bike', bike_id=bike_id))
    return render_template('add_part.html', title='Add Part', bike_id=bike_id, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('userhome', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Owner(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('userhome', username=user.username))
    return render_template('register.html', title='Register', form=form)

@app.route('/read')
def read():
    owners = Owner.query.all()
    for owner in owners:
        print("username:", owner.username)
        print("email:", owner.email)
        print("id:", owner.id)
    return "Read successful"



# ## Strava stuff
# @app.route('/strava')
# @login_required
# def strava_auth(user):
#     username = current_user.username
#     url = client.authorization_url(client_id=os.getenv('CLIENT_ID'), 
#                                redirect_uri=f'http://127.0.0.1:5000/user/{username}', 
#                                approval_prompt='auto')
    


if __name__ == "__main__":
    app.run(debug=True)
