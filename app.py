from flask import Flask, render_template

#create a Flask instance
app = Flask(__name__)

#create a route decrorator
@app.route('/')

def index():
    name = 'Jumbo'
    stuff = 'This is <strong>Bold Text</strong>'
    fruit = ['apple', 'orange', 'grapes']
    return render_template('index.html', name=name, stuff=stuff, fruit=fruit)


@app.route('/user/<name>')
def user(name):
    #return f'<h1>Hello {name}</h1>'
    return render_template('user.html', name=name)


#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500