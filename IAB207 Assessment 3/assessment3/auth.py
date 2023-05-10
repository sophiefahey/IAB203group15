from flask import Blueprint, render_template, request
from flask import session



bookingsbp = Blueprint('bookings',__name__)

@bookingsbp.route("/bookings")
def bookings():
    return render_template("user_booking_history.html")
