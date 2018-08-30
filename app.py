import os
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# Get the folder where this file runs
basedir = os.path.abspath(os.path.dirname(__file__))
    
# Configuration
DATABASE = 'flaskr.db'
DEBUG = True 
SECRET_KEY = 'son_of_a_gun'
USERNAME = 'admin'
PASSWORD = 'admin'


# Define the full path for the Database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# Database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models

'''
# Connect to Database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# Create the Database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
# Open Database Connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close Database Connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
'''
     
@app.route('/')
def index():
    # Searches the database for entries, then displays them
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    '''Add new post to database'''
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # User login/authentication/session management
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    #User logout/authentication/session management
    session.pop('logged_in', None)
    flash('You were successfully logged out')
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    '''Delete post from database'''
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': 'Post Deleted'}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)