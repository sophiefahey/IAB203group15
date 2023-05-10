from flask import Blueprint, render_template, request
from flask import session
#from .models import Event, Comment
#from .forms import EventForm

eventbp = Blueprint('events',__name__, url_prefix='/events/')

#refering to events/
@eventbp.route("/")
def events():
    return render_template("./events/event_details.html")