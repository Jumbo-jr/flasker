from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, email_validator
from pymongo import MongoClient

client = MongoClient('mongodb://advdatabase:codepi11@cluster0-shard-00-00.rhamq.mongodb.net:27017,cluster0-shard-00-01.rhamq.mongodb.net:27017,cluster0-shard-00-02.rhamq.mongodb.net:27017/myDB?ssl=true&replicaSet=atlas-hky1kt-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client['myDB']

class NamerForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = db.users.count_documents({'username':username.data})
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = db.users.count_documents({'email':email.data})
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SubmitForm(FlaskForm):
    #code = TextAreaField('Your code')
    submit = SubmitField('Submit')