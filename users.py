from cmath import exp
import email
from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager
from flask import render_template, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask import request

from flask_login import current_user, login_user, logout_user, login_required
import app

'''
client = MongoClient('mongodb://advdatabase:codepi11@cluster0-shard-00-00.rhamq.mongodb.net:27017,cluster0-shard-00-01.rhamq.mongodb.net:27017,cluster0-shard-00-02.rhamq.mongodb.net:27017/myDB?ssl=true&replicaSet=atlas-hky1kt-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client['myDB']




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
'''
class User:
    def __init__(self, _id, username, email, password, xp, date_added):
        self._id = _id
        self.username = username
        self.email = email
        self.xp = xp
        self.current_question = 1
        self.date_added = date_added
        self.profile_image = 'default.jpg'

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return app.bcrypt.check_password_hash(password_hash, password)


 