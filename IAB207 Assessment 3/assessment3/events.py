from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment 
from .forms import EventForm, CommentForm
from . import db 
import os 
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
#from flask import session
#from .models import Event, Comment
#from .forms import EventForm

eventbp = Blueprint('events',__name__, url_prefix='/events/')

#refering to events/
@eventbp.route("/<id>")
def events():
    event = db.session.scalar(db.select(event).where(Event.id==id))
    #creating comment form
    form = CommentForm()
    return render_template('./events/event_details.html', event=event, form=form)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        #check and return image
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data, image=form.image.data, description=form.description.data, date=form.date.data, time=form.time.data, location=form.location.data, category=form.category.data, member=form.member.data, nonMember=form.nonMember.data, concession=form.concession.data, student=form.student.data)
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
    return render_template('event_creation_update.html', event=event, form=form)


def check_upload_file(form):
    #get file data from form
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    db_upload_path = '/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


@eventbp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id==event))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, event=event, user=current_user)
        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been added', 'success')
        return redirect(url_for('event_details', id=event.id))


        
        
