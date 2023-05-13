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


    


    def _init_(self, name, image, description, date, time, location, category):
        self.name = name
        self.image = image
        self.description = description
        self.date = date 
        self.time = time
        self.location = location 
        self.category = category 
        self.comments = list()

    
    def set_comments(self, comment):
        self.comments.append(comment)

    