from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                            DataRequired(), 
                            Length(min=4, max=20)])
    email = EmailField('Email',
                        validators=[
                        DataRequired(),
                        Email()])
    password = PasswordField('Password',
                            validators=[
                            DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[
                                    DataRequired(),
                                    EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken, choose another')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email linked to an account - Log In')

class LoginForm(FlaskForm):
    email = EmailField('Email',
                        validators=[
                        DataRequired(),
                        Email()])
    password = PasswordField('Password',
                            validators=[
                            DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                            DataRequired(), 
                            Length(min=4, max=20)])
    email = EmailField('Email',
                        validators=[
                        DataRequired(),
                        Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken, choose another')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken, choose another')
            
class AddVehicleForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    submit = SubmitField('Add vehicle')
