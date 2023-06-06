import os
from flask import Flask
from flask import session
from flask import Blueprint, render_template, request, redirect, url_for,  flash
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from forms import RegisterForm, LoginForm, EventForm, CommentForm
from datetime import datetime, time, date
from models import db
from models import Cookuser, Event, Comment
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Set the upload folder!!!
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Specify the allowed extensions for file uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Each event details
@app.route('/event_details/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    userid = session.get('userid', None)
    event = Event.query.get(event_id)  # Retrieve the event from the database using the event_id
    if event:
        return render_template('event_details.html', event=event, userid=userid)
    else:
        # Handle event not found case
        return render_template('error.html', message='Event not found')
    
@app.route('/event/<event_id>/comment', methods=['POST'])
def add_comment(event_id):
    # Get the comment data from the form
    comment = request.form.get('comment')
    
    # Add your logic to process the comment, e.g., store it in a database
    
    # Retrieve the event with the updated comment
    event = Event.query.get(event_id)  # Retrieve the event from the database using the event_id
    
    # Render the event details template with the updated event data
    return render_template('event_details.html', event=event)

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
        user_id = session.get('userid', None)
        description = request.form.get('description')
        date_str = request.form.get('date')  # Get the date as a string
        time_str = request.form.get('time')  # Get the time as a string
        address = request.form.get('address')
        states = request.form.get('states')
        postgraduate = request.form.get('postgraduate')
        student = request.form.get('student')
        concession = request.form.get('concession')
        category = request.form.get('category')
        status = request.form.get('status')
        event_date = datetime.combine(date.fromisoformat(date_str), time.fromisoformat(time_str))  # Combine date and time
        event_time = time.fromisoformat(time_str)  # Convert time string to time object
        # Save the uploaded image
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            event_image = 'uploads/' + filename  # Store the image path in the database
            event = Event(user_id=user_id, title=title, description=description, date=event_date, time=event_time, address=address, image=event_image, postgraduate=postgraduate, student=student, concession=concession, category=category, status=status, states=states)
        else:
            event = Event(user_id=user_id, title=title, description=description, date=event_date, time=event_time, address=address,postgraduate=postgraduate, student=student, concession=concession, category=category, status=status, states=states)

        db.session.add(event)
        db.session.commit()

        return redirect('/events/')
    return render_template('create_event.html', form=form, userid=userid)

@app.route('/event_details/<event_id>/update', methods=['GET', 'POST'])
def edit(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        time_str = request.form['time']
        address = request.form['address']
        states = request.form['states']
        postgraduate = request.form['postgraduate']
        student = request.form['student']
        concession = request.form['concession']
        category = request.form['category']
        status = request.form['status']
        
        # Combine date and time
        event.title = title
        event.description = description
        event.date_str = date_str
        event.time_str = time_str
        event.address = address
        event.states = states
        event.postgraduate = postgraduate
        event.student = student
        event.category = category
        event.concession = concession
        event.status = status
        event.date = datetime.combine(date.fromisoformat(event.date_str), time.fromisoformat(event.time_str)) 
        event.time = time.fromisoformat(event.time_str)

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('events'))

    return render_template('event_creation_update.html', event=event)

@app.route('/event_details/<event_id>/delete', methods=['GET', 'POST'])
def delete(event_id):
    events = Event.query.get_or_404(event_id)
    db.session.delete(events)
    db.session.commit()
    return redirect('/events/')

#Events
@app.route('/events/')
def events():
    userid = session.get('userid', None)
    events = Event.query.all()
    form = EventForm
    return render_template('events.html', events=events, userid=userid, form=form)


#Booking
@app.route('/event_details/<event_id>/book', methods=['GET', 'POST'])
def book(event_id):
    book = BookingForm()
    event = Event.query.get_or_404(event_id)
    userid = session.get('userid', None)

    if book.validate_on_submit():
        
        booked_event = event.id
        order = random.randint(0, 10000000000000)

        booked_postgraduate = (int)(request.form['booked_postgraduate'])
        booked_student = (int)(request.form['booked_student'])
        booked_concession = (int)(request.form['booked_concession'])

        if booked_student == event.student and booked_postgraduate == event.postgraduate and booked_concession == event.concession:
            lol = "SoldOut"
            flash(f'Booking Successful for {userid}. Your OrderId is {order}', 'success')
            booking = Booking(order=order, userid=userid,  booked_eventid=booked_event, booked_student=booked_student, booked_postgraduate=booked_postgraduate, booked_concession=booked_concession)
            db.session.add(booking)
            if booked_student>-1 or booked_concession>-1 or booked_student>-1:
                new_s = event.student - booked_student
                new_c = event.concession - booked_concession
                new_p = event.postgraduate - booked_postgraduate
                Event.query.filter(Event.id==booked_event).update(dict(student= new_s))
                Event.query.filter(Event.id==booked_event).update(dict(concession= new_c))
                Event.query.filter(Event.id==booked_event).update(dict(postgraduate= new_p))
                Event.query.filter(Event.id==booked_event).update(dict(status=lol))
                return redirect('/events/')
            return redirect('/events/')
            
        elif booked_student > event.student or booked_postgraduate > event.postgraduate or booked_concession > event.concession:
            flash('Number of Tickets Entered Exceeds Number of Tickets Available', 'error')
            return redirect(url_for('event_details', event_id=event.id))

        elif booked_student == -1 and booked_postgraduate == -1 and booked_concession == -1:
            flash('No Tickets Were Selected', 'error')
            return redirect(url_for('event_details', event_id=event.id))

        elif booked_student==event.student and event.concession==0 and event.postgraduate==0:
            event.status = "SoldOut"
            flash(f'Booking Successful for {userid}. Your OrderId is {order}', 'success')
            return redirect(url_for('events'))
        elif event.student==0 and event.concession==booked_concession and event.postgraduate==0:
            print("pop")
            event.status = "SoldOut"
            flash(f'Booking Successful for {userid}. Your OrderId is {order}', 'success')
            return redirect(url_for('events'))
        elif event.student==0 and event.concession==0 and event.postgraduate==booked_postgraduate:
            print("cool")
            event.status = "SoldOut"
            flash(f'Booking Successful for {userid}. Your OrderId is {order}', 'success')
            return redirect(url_for('events'))
        else: 
            booking = Booking(order=order, userid=userid,  booked_eventid=booked_event, booked_student=booked_student, booked_postgraduate=booked_postgraduate, booked_concession=booked_concession)
            db.session.add(booking)
            flash(f'Booking Successful for {userid}. Your OrderId is {order}', 'success')
            if booked_student>-1:
                new_s = event.student - booked_student
                Event.query.filter(Event.id==booked_event).update(dict(student= new_s))
            if booked_concession>-1:
                new_c = event.concession - booked_concession
                Event.query.filter(Event.id==booked_event).update(dict(concession= new_c))
            if booked_postgraduate>-1:
                new_p = event.postgraduate - booked_postgraduate
                Event.query.filter(Event.id==booked_event).update(dict(postgraduate= new_p))
            return redirect(url_for('events'))
    return render_template('book.html', user_id= userid, event=event, form=book)



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
        return redirect('/login/')
    return render_template('register.html', form=form)

from sqlalchemy import desc

#search bar
@app.route('/search',methods=['GET'])
def search():
        userid = session.get('userid', None)
        query_res = request.args['search']
        
        if query_res == "IT" or query_res == "Engineering" or query_res == "Arts" or query_res == "Education" or query_res == "Business":
            events = Event.query.filter(Event.category==query_res)
            
        else:
            events = Event.query.filter(Event.title==query_res)
            

            return render_template('index.html', events=events, userid=userid)
        return render_template('index.html', events=events, userid=userid)
  

#search bar for event details
@app.route('/events/search',methods=['GET'])
def event_search():
        userid = session.get('userid', None)
        query_res = request.args['search']
        
        if query_res == "IT" or query_res == "it" or query_res == "iT" or query_res == "It":
            events = Event.query.filter(Event.category=="IT")
        elif query_res == "Engineering" or query_res == "engineering" or query_res == "engine":
            events = Event.query.filter(Event.category=="Engineering")
        elif query_res == "arts" or query_res == "Arts":
            events = Event.query.filter(Event.category=="Arts")
        elif query_res == "education" or query_res == "Education":
            events = Event.query.filter(Event.category=="Education")
        elif query_res == "business" or query_res == "Business":
            events = Event.query.filter(Event.category=="Business")
        else:
            events = Event.query.filter(Event.title==query_res)
            if query_res == "?":
                print("hey")
            

            return render_template('events.html', events=events, userid=userid)
        return render_template('events.html', events=events, userid=userid)
    
# Defualt link to index
@app.route('/', methods=['GET'])
def index():
    userid = session.get('userid', None)
    events = Event.query.all()
    return render_template('index.html', events=events, userid=userid)


bootstrap = Bootstrap(app)

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'rlacksdncjswoqkqhdkslek'
    app.config['SESSION_COOKIE_DOMAIN']= False
    

    # CSRF setting
    csrf = CSRFProtect()
    csrf.init_app(app)
    

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