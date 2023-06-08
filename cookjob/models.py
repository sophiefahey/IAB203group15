from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import url_for

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
    image = db.Column(db.String(255))
    postgraduate = db.Column(db.Integer, nullable=False)
    student = db.Column(db.Integer, nullable=False)
    concession = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='event', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"Event(id={self.id}, title='{self.title}', date='{self.date}')"

    @property
    def image_url(self):
        if self.image:
            return url_for('static', filename=f'uploads/{self.image}', _external=True)
        else:
            return url_for('static', filename='uploads/default_image.png', _external=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, nullable=False)
    commenter_username = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Comment: {}>".format(self.comment)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id=db.Column(db.Integer, primary_key=True, unique=True)
    order=db.Column(db.Integer, unique=True)
    userid =db.Column(db.String(100), db.ForeignKey('cookuser.id'))
    booked_eventid = db.Column(db.Integer, db.ForeignKey('events.id'))
    booked_student = db.Column(db.Integer, nullable=False)
    booked_concession = db.Column(db.Integer, nullable=False)
    booked_postgraduate = db.Column(db.Integer, nullable=False)