import os
from flask import Flask, url_for, request, session, redirect, render_template
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import RegisterForm, LoginForm, EventForm
from datetime import datetime, time, date
from models import db, Cookuser, Event
from flask_migrate import Migrate

app = Flask(__name__)
# Set the upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Specify the allowed extensions for file uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rlacksdncjswoqkqhdkslek'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Each event details
@app.route('/event_details/<int:event_id>', methods=['GET'])
def event_details(event_id):
    userid = session.get('userid', None)
    event = Event.query.get(event_id)

    if event:
        return render_template('event_details.html', event=event, userid=userid)
    else:
        return render_template('error.html', message='Event not found')

# User booking history
@app.route('/user_booking_history', methods=['GET', 'POST'])
def user_booking_history():
    return render_template('user_booking_history.html')

# Event creation
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    userid = session.get('userid', None)
    form = EventForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        location = request.form.get('location')

        event_date = datetime.combine(date.fromisoformat(date_str), time.fromisoformat(time_str))
        event_time = time.fromisoformat(time_str)

        # Save the uploaded image
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            event_image = 'uploads/' + filename  # Store the image path in the database
            event = Event(title=title, description=description, date=event_date, time=event_time, location=location, image=event_image)
        else:
            event = Event(title=title, description=description, date=event_date, time=event_time, location=location)

        db.session.add(event)
        db.session.commit()

        return redirect('/events/')

    return render_template('create_event.html', form=form, userid=userid)

# Events listing
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
        session['userid'] = form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cookuser = Cookuser()
        cookuser.userid = form.data.get('userid')
        cookuser.username = form.data.get('username')
        cookuser.password = form.data.get('password')

        db.session.add(cookuser)
        db.session.commit()

        print('success')

        return redirect('/')
    return render_template('register.html', form=form)

# Default index page
@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template('index.html', userid=userid)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
