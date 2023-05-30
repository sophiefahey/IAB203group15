import os
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask_wtf.csrf import CSRFProtect

from forms import RegisterForm, LoginForm, EventForm
from datetime import datetime, time, date

from models import db
from models import Cookuser, Event

app = Flask(__name__)

# Each event details
@app.route('/event_details/<int:event_id>', methods=['GET'])
def event_details(event_id):
    userid = session.get('userid', None)
    event = Event.query.get(event_id)  # Retrieve the event from the database using the event_id

    if event:
        return render_template('event_details.html', event=event, userid=userid)
    else:
        # Handle event not found case
        return render_template('error.html', message='Event not found')

# User_booking_history
@app.route('/user_booking_history', methods=['GET', 'POST'])
def user_booking_history():
    return render_template('user_booking_history.html')

# Event creation
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    userid = session.get('userid', None)
    form = EventForm()  # Instantiate the EventForm
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')  # Get the date as a string
        time_str = request.form.get('time')  # Get the time as a string
        location = request.form.get('location')

        event_date = datetime.combine(date.fromisoformat(date_str), time.fromisoformat(time_str))  # Combine date and time
        event_time = time.fromisoformat(time_str)  # Convert time string to time object

        event = Event(title=title, description=description, date=event_date, time=event_time, location=location)  # Create an instance of Event
        db.session.add(event)  # Add the instance to the session
        db.session.commit()  # Commit the changes to the database

        return redirect('/events/')

    return render_template('create_event.html', form=form, userid=userid)

@app.route('/events/')
def events():
    userid = session.get('userid', None)
    events = Event.query.all()
    return render_template('events.html', events=events, userid=userid)

# Logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

# Login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get userid from the database
        session['userid'] = form.data.get('userid')
        return redirect('/')
    
    return render_template('login.html', form=form)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get register form fromRegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        cookuser = Cookuser()
        cookuser.userid = form.data.get('userid')
        cookuser.username = form.data.get('username')
        cookuser.password = form.data.get('password')

        # Send user details to the DB
        db.session.add(cookuser)
        db.session.commit()

        print('success')

        return redirect('/')
    return render_template('register.html', form=form)

# Defualt link to index
@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template('index.html', userid=userid)

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'rlacksdncjswoqkqhdkslek'

    # CSRF setting
    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)
    db.app = app
    # Set up the application context
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)

# Cache control
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response