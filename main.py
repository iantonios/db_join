# This example illustrates SQLAlchemy functionality.  It's
# intenteded to be run using the Flask shell, not as Flask
# application since no routes are defined.

# Steps to run:
# 1. export FLASK_APP=main.py
# 2. Start shell mode: python3 -m flask shell
# 3. Import main and db:
#    import main
#    from main import db

# 4. Create sqlite schema: db.create_all()

# 5. Add users: main.add_users()
# 6. Add posts: main.add_posts()
# 7. View results of a different join operations:
#    main.view_posts()
#    main.view_posts_filter()

# SQLAlchemy documentation (scroll down to join):
# https://docs.sqlalchemy.org/en/13/orm/query.html


import os
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

def add_users():

    users = ['susan', 'rob', 'joe', 'jill', 'tom', 'jen', 'zoe']
    emails_domains = ['@gmail.com', '@outlook.com', '@msn.com']

    # add 10 random users
    for i in range(10):
        user = random.choice(users) + str(i)
        domain = random.choice(emails_domains)
        u = User(username=user, email=user+domain)
        db.session.add(u)

    db.session.commit()
    return 'Done'

def add_posts():
    # Add posts to 30 randomly selected users (a user can be selected
    # more than once)
    for i in range(30):
        num = random.randint(1, 10)
        u = User.query.get(num)
        p = Post(body='post ' + str(i), author=u)
        db.session.add(p)

    db.session.commit()
    return 'Done'

def view_posts():
    results = db.session.query(User, Post).join(Post)
    print('SQL Query: \n', results.statement.compile(dialect=db.session.bind.dialect))
    print('\n\nResults:')
    for row in results:
        print(row)

def view_posts_filter():
    username = input('Input username to look for: ')
    results = db.session.query(User, Post).join(Post).filter(User.username==username)
    print('SQL Query: \n', results.statement.compile(dialect=db.session.bind.dialect))
    print('\n\nResults:')
    for row in results:
        print(row)
