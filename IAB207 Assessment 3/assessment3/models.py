from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DB setting for app user
class Cookuser(db.Model):
    __tablename__ = 'cookuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

# DB for event creation
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Event(id={self.id}, title='{self.title}', date='{self.date}')"