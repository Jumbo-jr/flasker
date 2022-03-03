from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, logout_user, current_user
from forms import NamerForm, RegisterForm, LoginForm, SubmitForm

from users import User


client = MongoClient('mongodb://advdatabase:codepi11@cluster0-shard-00-00.rhamq.mongodb.net:27017,cluster0-shard-00-01.rhamq.mongodb.net:27017,cluster0-shard-00-02.rhamq.mongodb.net:27017/myDB?ssl=true&replicaSet=atlas-hky1kt-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client['myDB']



#create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is some secret key'
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({"username": username})
    if not user:
        return None
    return User(user[str('_id')],user['username'], user['email'], user['password'], user['xp'], user['date_added'])

import users







#create a route decrorator
@app.route('/')
def index():
    form = SubmitForm()
    return render_template('index.html',question=db.questions.find_one(), form=form)


@app.route('/about/')
def hello():
    name = 'Jumbo'
    stuff = 'This is <strong>Bold Text</strong>'
    fruit = ['apple', 'orange', 'grapes']
    return render_template('hello.html', name=name, stuff=stuff, fruit=fruit)


@app.route('/user/<name>')
def user(name):
    #return f'<h1>Hello {name}</h1>'
    return render_template('user.html', name=name)


#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/name', methods=['POST', 'GET'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfully!', 'info')
    return render_template('name.html', name=name, form=form)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()



    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = {
            'username':form.username.data,
            'email':form.email.data,
            'password':hashed_password,
            'xp':16,
            'current_question':1,
            'profile_image':'default.jpg',
            'date_added':str(datetime.now()).split('.')[0]
        }
        db.users.insert_one(user)

        flash(f'Your account has been created! You are now log in.', 'info')
        _id = str(db.users.find_one({'username':user['username']}))

        user_obj = User(_id,user['username'], user['email'], user['password'], user['xp'], user['date_added'])
        login_user(user_obj)

        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({'email':form.email.data})

        if user:
            if bcrypt.check_password_hash(user['password'], form.password.data):
                flash('You have been logged in!', 'warning')
                
                db.users.update_one({'email':user['email']},{'$inc':{'xp':41}})
                user_obj = User(str(user['_id']),user['username'], user['email'], user['password'], user['xp'], user['date_added'])
                login_user(user_obj)

                return redirect(url_for('index'))
            else:
                flash('Wrong Password - Try Again!', 'danger')
        else:
            flash('That email doesn\'t exist! - please try again.', 'danger')
        #if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            #flash('You have been logged in!', 'success')
            #return redirect(url_for('index'))
        
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'warning')
    return redirect(url_for('login'))

@app.route('/profile/', methods=['GET','POST'])
@login_required
def profile():
    return render_template('profile.html')
