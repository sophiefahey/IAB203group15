from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# DB setting for app user
class Cookuser(db.Model):
    __tablename__ = 'cookuser'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80))
    phonenumber = db.Column(db.String(12))
    email= db.Column(db.String(40))
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

# DB for event creation
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    states = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))  # Use URLType to store the image URL
    postgraduate = db.Column(db.Integer, nullable=False)
    student = db.Column(db.Integer, nullable=False)
    concession = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    #cookuser_id = db.Column(db.Integer, db.ForeignKey('cookuser.id'))

    def __repr__(self):
        return f"Event(id={self.id}, title='{self.title}', date='{self.date}')"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('cookuser.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
