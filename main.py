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
    u1 = User(username='susan', email='susan@example.com')
    u2 = User(username='joe', email='joe@example.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    return 'Done'

def add_posts():
    u = User.query.get(1)
    p = Post(body='first post, susan', author=u)
    db.session.add(p)
    p = Post(body='second post, susan', author=u)
    db.session.add(p)

    u = User.query.get(2)
    p = Post(body='first post, joe', author=u)
    db.session.add(p)
    p = Post(body='second post, joe', author=u)
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
    results = db.session.query(User, Post).join(Post).filter(User.username=='susan')
    print('SQL Query: \n', results.statement.compile(dialect=db.session.bind.dialect))
    print('\n\nResults:')
    for row in results:
        print(row)
