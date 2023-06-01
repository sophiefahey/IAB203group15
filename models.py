from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

# DB setting for app user
class Cookuser(db.Model):
    __tablename__ = 'cookuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

# DB setting for event creation
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)   
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)  # Change the column type to Date
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))  # Use URLType to store the image URL

    def __repr__(self):
        return f"Event(id={self.id}, title='{self.title}', date='{self.date}')"

    @property
    def formatted_date(self):
        if isinstance(self.date, str) and len(self.date) == 4:
            # Handle the string format 'YYYY' instead of 'YYYY-MM-DD'
            formatted_date = datetime.strptime(self.date, '%Y').strftime("%B %d, %Y")
        else:
            formatted_date = self.date.strftime("%B %d, %Y")
        return formatted_date
