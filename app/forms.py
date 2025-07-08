from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
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

class UpdateVehicleForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    vin = StringField('VIN', validators=[Optional()])
    color = StringField('Color', validators=[Optional()])
    engine_type = SelectField('Engine Type', choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric')], validators=[Optional()])
    engine_model = StringField('Engine Model', validators=[Optional()])
    engine_number = StringField('Engine Number', validators=[Optional()])
    transmission_type = StringField('Transmission Type', validators=[Optional()])
    transmission_model = StringField('Transmission Model', validators=[Optional()])
    tax_start_date = DateField('Tax Start Date', format='%Y-%m-%d', validators=[Optional()])
    tax_end_date = DateField('Tax End Date', format='%Y-%m-%d', validators=[Optional()])
    insurance_start_date = DateField('Insurance Start Date', format='%Y-%m-%d', validators=[Optional()])
    insurance_end_date = DateField('Insurance End Date', format='%Y-%m-%d', validators=[Optional()])
    registration_scan = FileField('Registration Scan', validators=[Optional()])
    insurance_scan = FileField('Insurance Scan', validators=[Optional()])
    submit = SubmitField('Update Vehicle')
