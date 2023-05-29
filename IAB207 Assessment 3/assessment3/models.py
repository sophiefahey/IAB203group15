from . import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users' # table name 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True, nullable = False)
    emailid = db.Column(db.String(100), index = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    comments = db.relationship('Comment', backref = 'user')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    image = db.Column(db.String(400))
    description = db.Column(db.String(200))
    date = db.Column(db.Date(8))
    time = db.Column(db.Time(4))
    location = db.Column(db.String(100))
    category = db.Column(db.String(80))
    comments = db.relationship('Comment', backref = 'events')

    def __repr__(self): 
        return "<Name: {}>".format(self.name)
    


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default = datetime.now())
    #add foreign keys 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
    
    