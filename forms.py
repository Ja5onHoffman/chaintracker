from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, SelectMultipleField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import Owner, Bike, Part
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')]) 
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Owner.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = Owner.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PartForm(FlaskForm):
    name = StringField('Part Name', validators=[DataRequired()])
    part_type = SelectField('Part Type', choices=[('type1', 'Type 1'), ('type2', 'Type 2')], validators=[DataRequired()])
    miles = StringField('Miles', validators=[DataRequired()])
    hours = StringField('Hours', validators=[DataRequired()])
    mile_limit = StringField('Mile Limit', validators=[DataRequired()])
    hour_limit = StringField('Hour Limit', validators=[DataRequired()])
    submit = SubmitField('Add Part')
        
class BikeForm(FlaskForm):
    bikes = SelectField('Select a Bike', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Add Bike')



# class BikeFromStrava(FlaskForm):
#     name = SelectField('Bike', coerce=int)