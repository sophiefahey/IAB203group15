from . import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users' # table name 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True, nullable = False)
    emailid = db.Column(db.String(100), index = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    comments = db.relationship('Comment', backref = 'user')


class Event:

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

    